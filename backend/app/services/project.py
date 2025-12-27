from datetime import datetime, timedelta
from typing import List, Optional

from app.dbmodels import Client, LoggedHour, Project, ProjectMember, Task, User
from app.schemas.project import (
    ClientPortalProject,
    HealthFlag,
    ProjectCreate,
    ProjectHealth,
    ProjectHealthIndicator,
    ProjectMemberCreate,
    ProjectStatistics,
    ProjectUpdate,
    TaskCount,
)
from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session


class ProjectService:
    @staticmethod
    def create_project(
        db: Session,
        project_in: ProjectCreate,
        current_user_id: int,  # pylint: disable=unused-argument
    ) -> Project:
        """Create a new project."""
        # Verify client exists
        client = db.query(Client).filter(Client.id == project_in.client_id).first()
        if not client:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")

        # Create project
        db_project = Project(
            name=project_in.name,
            description=project_in.description,
            status=project_in.status,
            client_id=project_in.client_id,
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
        db: Session, project_id: int, user_id: int, is_admin: bool = False
    ) -> Project:
        """Get a project with access control check."""
        project = ProjectService.get_project(db, project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        if is_admin:
            # Populate member stats even for admins
            ProjectService._populate_member_stats(db, project_id, project.members)
            return project

        # Check membership for non-admin users
        member = (
            db.query(ProjectMember)
            .filter(ProjectMember.project_id == project_id, ProjectMember.user_id == user_id)
            .first()
        )

        if member:
            # Populate member stats for the project's members list
            # This ensures get_project returns members with task_count populated
            ProjectService._populate_member_stats(db, project_id, project.members)
            return project

        # Check for project owner (the user who created the client for this project)
        client = db.query(Client).filter(Client.id == project.client_id).first()
        if client and client.created_by == user_id:
            # Populate member stats for the project's members list
            ProjectService._populate_member_stats(db, project_id, project.members)
            return project

        raise HTTPException(status_code=403, detail="Not a member or owner of this project")

    @staticmethod
    def is_project_owner(db: Session, project_id: int, user_id: int) -> bool:
        """Check if a user is the owner (creator of the client) of a project."""
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            return False
        client = db.query(Client).filter(Client.id == project.client_id).first()
        return bool(client and client.created_by == user_id)

    @staticmethod
    def list_projects(
        db: Session,
        user_id: int,
        is_admin: bool = False,
        client_id: Optional[int] = None,
        status_filter: Optional[str] = None,
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
        is_admin: bool = False,
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
        existing = (
            db.query(ProjectMember)
            .filter(
                ProjectMember.project_id == project_id, ProjectMember.user_id == member_in.user_id
            )
            .first()
        )
        if existing:
            raise HTTPException(status_code=400, detail="User already a member")

        new_member = ProjectMember(
            project_id=project_id,
            user_id=member_in.user_id,
            role=member_in.role,
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
        member = (
            db.query(ProjectMember)
            .filter(ProjectMember.project_id == project_id, ProjectMember.user_id == user_id)
            .first()
        )

        if not member:
            raise HTTPException(status_code=404, detail="Member not found")

        db.delete(member)
        db.commit()
        return member

    @staticmethod
    def _populate_member_stats(db: Session, project_id: int, members: List[ProjectMember]):
        """Helper to populate task_count for a list of project members."""
        now_time = datetime.now()
        for member in members:
            # Calculate logged hours
            hours_logged = (
                db.query(func.sum(LoggedHour.hours))
                .filter(LoggedHour.project_id == project_id, LoggedHour.user_id == member.user_id)
                .scalar()
                or 0.0
            )

            # Base task query for this member in this project
            member_tasks = db.query(Task).filter(
                Task.project_id == project_id, Task.assigned_to == member.user_id
            )

            # Assign stats to member.task_count (will be picked up by Pydantic)
            member.task_count = TaskCount(
                hours_logged=hours_logged,
                tasks_count=member_tasks.count(),
                completed_tasks_count=member_tasks.filter(Task.status == "completed").count(),
                in_progress_tasks_count=member_tasks.filter(Task.status == "in_progress").count(),
                todo_tasks_count=member_tasks.filter(Task.status == "todo").count(),
                overdue_tasks_count=member_tasks.filter(
                    Task.status != "completed", Task.due_date.isnot(None), Task.due_date < now_time
                ).count(),
            )

    @staticmethod
    def list_members(db: Session, project_id: int) -> List[ProjectMember]:
        """List all members of a project."""
        members = db.query(ProjectMember).filter(ProjectMember.project_id == project_id).all()
        ProjectService._populate_member_stats(db, project_id, members)
        return members

    # ==================================================get the statistics of a project==========================
    @staticmethod
    def get_project_statistics(db: Session, project_id: int) -> ProjectStatistics:
        """
        Get project statistics.

        Returns aggregated project statistics including:
        - Total logged hours
        - Task counts (total, completed, in-progress, overdue)
        - Member activity summary (hours per member, task count per member)
        """
        # Check if the project exists
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="This Project does not exist")

        # Get project members and their stats
        members = db.query(ProjectMember).filter(ProjectMember.project_id == project_id).all()
        ProjectService._populate_member_stats(db, project_id, members)
        now_time = datetime.now()

        # we have to get the project tasks
        tasks = db.query(Task).filter(Task.project_id == project_id).all()

        # then we have to check the task counts of an individual task in the task array and increment the counts according to their status
        total_tasks = len(tasks)
        total_completed_tasks = 0
        total_in_progress_tasks = 0
        total_todo_tasks = 0
        total_overdue_tasks = 0

        for task in tasks:
            if task.status == "completed":
                total_completed_tasks += 1
            elif task.status == "in_progress":
                total_in_progress_tasks += 1
            elif task.status == "todo":
                total_todo_tasks += 1

            # Check for overdue tasks (must have due_date and not be completed)
            if (
                task.status != "completed"
                and task.due_date is not None
                and now_time > task.due_date
            ):
                total_overdue_tasks += 1

        # Calculate total logged hours for the project
        total_logged_hours = (
            db.query(func.sum(LoggedHour.hours))
            .filter(LoggedHour.project_id == project_id)
            .scalar()
            or 0.0
        )
        # then we return the project statistics
        return ProjectStatistics(
            id=project.id,
            name=project.name,
            description=project.description,
            status=project.status,
            client_id=project.client_id,
            created_at=project.created_at,
            updated_at=project.updated_at,
            members=members,
            tasks=tasks,
            total_logged_hours=total_logged_hours,
            total_tasks=total_tasks,
            total_completed_tasks=total_completed_tasks,
            total_in_progress_tasks=total_in_progress_tasks,
            total_todo_tasks=total_todo_tasks,
            total_overdue_tasks=total_overdue_tasks,
        )

    # ==================================================get the health of a project==========================
    @staticmethod
    def get_project_health(db: Session, project_id: int) -> ProjectHealth:
        """
        Get project health indicators.

        Returns health indicators including:
        - Overdue tasks count
        - Inactive members (no hours logged in last 7 days)
        - Tasks with no assignee
        - Activity drop-off (last month vs previous month)
        """
        # Check if the project exists
        project = db.query(Project).filter(Project.id == project_id).first()

        if not project:
            raise HTTPException(status_code=404, detail="This Project does not exist")

        # to get a project health we will use these 4 indicators:
        # 1. we check for overdues tasks
        now_time = datetime.now()
        overdue_tasks = (
            db.query(Task)
            .filter(
                Task.project_id == project_id,
                Task.status != "completed",
                Task.due_date.isnot(None),
                Task.due_date < now_time,
            )
            .all()
        )
        overdue_count = len(overdue_tasks)
        overdue_indicator = ProjectHealthIndicator(
            status=HealthFlag.alert if overdue_count > 0 else HealthFlag.ok,
            message=f"{overdue_count} overdue tasks",
        )

        # 2. the seond is that we will have to check for inactive members that have no logged hours in the last N days
        # we will use the last 7 days as the threshold
        threshold_date = datetime.now() - timedelta(days=7)
        last_n_days = 7
        # Get all project members
        members = db.query(ProjectMember).filter(ProjectMember.project_id == project_id).all()
        inactive_members_list = []

        for member in members:
            # Check for logged hours in last N days
            recent_log = (
                db.query(LoggedHour)
                .filter(
                    LoggedHour.project_id == project_id,
                    LoggedHour.user_id == member.user_id,
                    LoggedHour.logged_at >= threshold_date,
                )
                .first()
            )

            if not recent_log:
                user = db.query(User).filter(User.id == member.user_id).first()
                if user:
                    inactive_members_list.append(
                        {"id": user.id, "name": f"{user.first_name} {user.last_name}"}
                    )

        inactive_indicator = ProjectHealthIndicator(
            status=HealthFlag.warning if inactive_members_list else HealthFlag.ok,
            message=f"{len(inactive_members_list)} inactive members in the last {last_n_days} days",
            details={"members": inactive_members_list} if inactive_members_list else None,
        )

        # 3. The third is that we will check for tasks with no assignee
        unassigned_tasks = (
            db.query(Task).filter(Task.project_id == project_id, Task.assigned_to.is_(None)).all()
        )
        unassigned_count = len(unassigned_tasks)
        unassigned_details = [{"id": t.id, "title": t.title} for t in unassigned_tasks]

        unassigned_indicator = ProjectHealthIndicator(
            status=HealthFlag.info if unassigned_count > 0 else HealthFlag.ok,
            message=f"{unassigned_count} tasks with no assignees",
            details={"tasks": unassigned_details} if unassigned_details else None,
        )

        # 5. Activity Drop-off (last month vs previous month)
        # We compare count of completed tasks or updated tasks. Let's use tasks completed.
        now_time = datetime.now()
        last_month_start = now_time - timedelta(days=30)
        prev_month_start = now_time - timedelta(days=60)

        last_month_activity = (
            db.query(Task)
            .filter(
                Task.project_id == project_id,
                Task.status == "completed",
                Task.updated_at >= last_month_start,
            )
            .count()
        )

        prev_month_activity = (
            db.query(Task)
            .filter(
                Task.project_id == project_id,
                Task.status == "completed",
                Task.updated_at >= prev_month_start,
                Task.updated_at < last_month_start,
            )
            .count()
        )

        dropoff_status = HealthFlag.ok
        if prev_month_activity > 0:
            if last_month_activity < prev_month_activity * 0.5:
                dropoff_status = HealthFlag.alert
            elif last_month_activity < prev_month_activity:
                dropoff_status = HealthFlag.warning

        activity_indicator = ProjectHealthIndicator(
            status=dropoff_status,
            message=f"Activity drop-off: {last_month_activity} vs {prev_month_activity} tasks completed",
            details={
                "last_month_count": last_month_activity,
                "previous_month_count": prev_month_activity,
            },
        )

        return ProjectHealth(
            project_id=project_id,
            overdue_tasks=overdue_indicator,
            inactive_members=inactive_indicator,
            unassigned_tasks=unassigned_indicator,
            activity_dropoff=activity_indicator,
        )

    @staticmethod
    def get_client_portal_project(
        db: Session, project_id: int, client: Client
    ) -> ClientPortalProject:
        """
        Fetch a project by ID and return a sanitized version for the Client Portal.
        Verifies that the project belongs to the given client.
        """
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

        if project.client_id != client.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have access to this project",
            )

        # Extract member names
        # Ensure we have the user names
        member_names = []
        for member in project.members:
            if member.user:
                name = f"{member.user.first_name} {member.user.last_name}"
                member_names.append(name)

        return ClientPortalProject(
            id=project.id,
            name=project.name,
            description=project.description,
            status=project.status,
            client_name=client.name,
            members=member_names,
            created_at=project.created_at,
            updated_at=project.updated_at,
        )
