from typing import List, Optional
from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.database import GitContribution, Project, Task, ProjectMember, User
from app.schemas.git_contribution import GitContributionCreate, GitContributionUpdate


class GitContributionService:
    @staticmethod
    def _check_project_membership(
        db: Session,
        project_id: int,
        user_id: int,
        is_admin: bool = False
    ) -> bool:
        """Check if user is a member of the project."""
        if is_admin:
            return True

        member = db.query(ProjectMember).filter(
            ProjectMember.project_id == project_id,
            ProjectMember.user_id == user_id
        ).first()

        return member is not None

    @staticmethod
    def _check_task_belongs_to_project(
        db: Session,
        task_id: int,
        project_id: int
    ) -> bool:
        """Check if task belongs to the project."""
        task = db.query(Task).filter(
            Task.id == task_id,
            Task.project_id == project_id
        ).first()

        return task is not None

    @staticmethod
    def create_contribution(
        db: Session,
        contribution_in: GitContributionCreate,
        current_user_id: int,
        is_admin: bool = False
    ) -> GitContribution:
        """
        Create a new git contribution.

        Business Rules:
        - User must be a member of the project
        - Same commit hash cannot be linked twice to the same project
        - If task_id is provided, task must belong to the project
        """
        # Verify project exists
        project = db.query(Project).filter(Project.id == contribution_in.project_id).first()
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )

        # Check project membership (unless admin)
        if not GitContributionService._check_project_membership(
            db, contribution_in.project_id, current_user_id, is_admin
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You must be a member of this project to create contributions"
            )

        # Verify user exists (if different from current user,
        # admin might be creating for someone else)
        user = db.query(User).filter(User.id == contribution_in.user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Only allow creating for self unless admin
        if not is_admin and contribution_in.user_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only create contributions for yourself"
            )

        # Check for duplicate commit hash in the same project
        existing = db.query(GitContribution).filter(
            GitContribution.project_id == contribution_in.project_id,
            GitContribution.commit_hash == contribution_in.commit_hash
        ).first()

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This commit hash is already linked to this project"
            )

        # Validate task if provided
        if contribution_in.task_id:
            if not GitContributionService._check_task_belongs_to_project(
                db, contribution_in.task_id, contribution_in.project_id
            ):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Task does not belong to this project"
                )

        # Create contribution
        now = datetime.now(timezone.utc)

        db_contribution = GitContribution(
            user_id=contribution_in.user_id,
            project_id=contribution_in.project_id,
            task_id=contribution_in.task_id,
            commit_hash=contribution_in.commit_hash,
            branch=contribution_in.branch,
            commit_message=contribution_in.commit_message,
            provider=contribution_in.provider,
            commit_url=contribution_in.commit_url,
            # Set for database compatibility (legacy column with NOT NULL constraint)
            committed_at=now
        )

        db.add(db_contribution)
        db.commit()
        db.refresh(db_contribution)

        return db_contribution

    @staticmethod
    def get_contribution(
        db: Session,
        contribution_id: int,
        current_user_id: int,
        is_admin: bool = False
    ) -> GitContribution:
        """
        Retrieve a contribution by ID.

        Business Rules:
        - User must be a member of the project (or admin)
        """
        contribution = db.query(GitContribution).filter(
            GitContribution.id == contribution_id
        ).first()

        if not contribution:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Contribution not found"
            )

        # Check project membership
        if not GitContributionService._check_project_membership(
            db, contribution.project_id, current_user_id, is_admin
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have access to this contribution"
            )

        return contribution

    @staticmethod
    def list_contributions(
        db: Session,
        current_user_id: int,
        is_admin: bool = False,
        user_id: Optional[int] = None,
        project_id: Optional[int] = None,
        provider: Optional[str] = None
    ) -> List[GitContribution]:
        """
        List contributions with optional filters.

        Business Rules:
        - Non-admin users can only see contributions from projects they are members of
        - Admins can see all contributions
        - Filters are combinable
        """
        query = db.query(GitContribution)

        # Apply filters
        if user_id:
            query = query.filter(GitContribution.user_id == user_id)

        if project_id:
            query = query.filter(GitContribution.project_id == project_id)

            # For non-admin users, verify project membership if filtering by project
            if not is_admin:
                if not GitContributionService._check_project_membership(
                    db, project_id, current_user_id, is_admin
                ):
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="You are not a member of this project"
                    )

        if provider:
            query = query.filter(GitContribution.provider == provider.lower())

        # For non-admin users, filter by project membership
        if not is_admin:
            # Get all project IDs where user is a member using a subquery
            member_project_ids = select(ProjectMember.project_id).where(
                ProjectMember.user_id == current_user_id
            ).scalar_subquery()

            query = query.filter(GitContribution.project_id.in_(member_project_ids))

        return query.all()

    @staticmethod
    def link_to_task(
        db: Session,
        contribution_id: int,
        task_id: Optional[int],
        current_user_id: int,
        is_admin: bool = False
    ) -> GitContribution:
        """
        Link a contribution to a task.

        Business Rules:
        - Only the contributor or admin can link a commit
        - Task must belong to the contribution's project
        """
        contribution = db.query(GitContribution).filter(
            GitContribution.id == contribution_id
        ).first()

        if not contribution:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Contribution not found"
            )

        # Check permission: only contributor or admin can link
        if not is_admin and contribution.user_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only the contributor or admin can link commits to tasks"
            )

        # Validate task if provided
        if task_id:
            if not GitContributionService._check_task_belongs_to_project(
                db, task_id, contribution.project_id
            ):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Task does not belong to this project"
                )

        # Update task link
        contribution.task_id = task_id
        db.add(contribution)
        db.commit()
        db.refresh(contribution)

        return contribution

    @staticmethod
    def update_contribution(
        db: Session,
        contribution_id: int,
        contribution_in: GitContributionUpdate,
        current_user_id: int,
        is_admin: bool = False
    ) -> GitContribution:
        """
        Update a contribution.

        Business Rules:
        - Only the contributor or admin can update
        - If updating task_id, task must belong to the contribution's project
        """
        contribution = db.query(GitContribution).filter(
            GitContribution.id == contribution_id
        ).first()

        if not contribution:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Contribution not found"
            )

        # Check permission: only contributor or admin can update
        if not is_admin and contribution.user_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only the contributor or admin can update contributions"
            )

        # Validate task if provided
        if contribution_in.task_id is not None:
            if contribution_in.task_id and not \
                    GitContributionService._check_task_belongs_to_project(
                db, contribution_in.task_id, contribution.project_id
            ):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Task does not belong to this project"
                )

        # Update fields
        update_data = contribution_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(contribution, field, value)

        db.add(contribution)
        db.commit()
        db.refresh(contribution)

        return contribution
