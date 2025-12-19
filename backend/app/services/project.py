from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.database import Project, ProjectMember, Client, User
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectMemberCreate


class ProjectService:
    @staticmethod
    def create_project(
        db: Session,
        project_in: ProjectCreate,
        current_user_id: int  # pylint: disable=unused-argument
    ) -> Project:
        """Create a new project."""
        # Verify client exists
        client = db.query(Client).filter(Client.id == project_in.client_id).first()
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Client not found"
            )

        # Create project
        db_project = Project(
            name=project_in.name,
            description=project_in.description,
            status=project_in.status,
            client_id=project_in.client_id
        )
        db.add(db_project)
        db.commit()
        db.refresh(db_project)

        return db_project

    @staticmethod
    def get_project(db: Session, project_id: int) -> Optional[Project]:
        """Get a project by ID."""
        return db.query(Project).filter(Project.id == project_id).first()

    @staticmethod
    def get_project_with_check(
        db: Session,
        project_id: int,
        user_id: int,
        is_admin: bool = False
    ) -> Project:
        """Get a project with access control check."""
        project = ProjectService.get_project(db, project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        if is_admin:
            return project

        # Check membership for non-admin users
        member = db.query(ProjectMember).filter(
            ProjectMember.project_id == project_id,
            ProjectMember.user_id == user_id
        ).first()

        if not member:
            raise HTTPException(status_code=403, detail="Not a member of this project")

        return project

    @staticmethod
    def list_projects(
        db: Session,
        user_id: int,
        is_admin: bool = False,
        client_id: Optional[int] = None,
        status_filter: Optional[str] = None
    ) -> List[Project]:
        """List projects with optional filters."""
        query = db.query(Project)

        if client_id:
            query = query.filter(Project.client_id == client_id)

        if status_filter:
            query = query.filter(Project.status == status_filter)

        if not is_admin:
            # Filter by membership for non-admin users
            query = query.join(ProjectMember).filter(ProjectMember.user_id == user_id)

        return query.all()

    @staticmethod
    def update_project(
        db: Session,
        project_id: int,
        project_in: ProjectUpdate,
        user_id: int,
        is_admin: bool = False
    ) -> Project:
        """Update a project."""
        project = ProjectService.get_project_with_check(db, project_id, user_id, is_admin)

        update_data = project_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(project, field, value)

        db.add(project)
        db.commit()
        db.refresh(project)
        return project

    @staticmethod
    def delete_project(db: Session, project_id: int) -> Project:
        """
        Delete a project.
        
        Note: Admin check should be done at the route level.
        """
        project = ProjectService.get_project(db, project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        db.delete(project)
        db.commit()
        return project

    @staticmethod
    def add_member(db: Session, project_id: int, member_in: ProjectMemberCreate) -> ProjectMember:
        """
        Add a member to a project.
        
        Note: Admin check should be done at the route level.
        """
        # Check if project exists
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        # Check if user exists
        user = db.query(User).filter(User.id == member_in.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Check if already member
        existing = db.query(ProjectMember).filter(
            ProjectMember.project_id == project_id,
            ProjectMember.user_id == member_in.user_id
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="User already a member")

        new_member = ProjectMember(
            project_id=project_id,
            user_id=member_in.user_id,
            role=member_in.role
        )
        db.add(new_member)
        db.commit()
        db.refresh(new_member)
        return new_member

    @staticmethod
    def remove_member(db: Session, project_id: int, user_id: int) -> ProjectMember:
        """
        Remove a member from a project.
        
        Note: Admin check should be done at the route level.
        """
        member = db.query(ProjectMember).filter(
            ProjectMember.project_id == project_id,
            ProjectMember.user_id == user_id
        ).first()

        if not member:
            raise HTTPException(status_code=404, detail="Member not found")

        db.delete(member)
        db.commit()
        return member

    @staticmethod
    def list_members(db: Session, project_id: int) -> List[ProjectMember]:
        """List all members of a project."""
        return db.query(ProjectMember).filter(ProjectMember.project_id == project_id).all()
