from sqlalchemy.sql.functions import now
from typing import List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.api.deps import get_current_project_member
from app.database import Project, ProjectMember, Client, User, Task, LoggedHour
from app.schemas.project import (
    ProjectCreate, 
    ProjectUpdate, 
    ProjectMemberCreate, 
    ProjectStatistics,
    ProjectHealth,
    ProjectHealthIndicator,
    HealthFlag
)


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

#==================================================get the statistics of a project==========================
    @staticmethod
    def get_project_statistics(db: Session, project_id: int) -> ProjectStatistics:
        """
        Get project statistics.
        """

        # we need to first check wether the current user is a member of the project and also find a project assigned to the project we are trying to look for depending on their id
        #member = get_current_project_member(project_id)


        #then we also need to check if the project exists at all
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="This Project does not exist")

        #we have to get the project members
        members = db.query(ProjectMember).filter(ProjectMember.project_id == project_id).all()
        
        #we have to get the project tasks
        tasks = db.query(Task).filter(Task.project_id == project_id).all()
        
        #then we have to check the task counts of an individual task in the task array and increment the counts according to their status
        total_tasks = len(tasks)
        total_completed_tasks = 0
        total_in_progress_tasks = 0
        total_on_hold_tasks = 0
        total_overdue_tasks = 0

        for task in tasks:
            if task.status == "completed":
                total_completed_tasks += 1
            elif task.status == "in_progress":
                total_in_progress_tasks += 1
            elif task.status == "on_hold":
                total_on_hold_tasks += 1
            elif task.status == "overdue":
                total_overdue_tasks += 1

        #then we have to get the total logged hours of the project
        total_logged_hours = project.total_logged_hours
        #then we return the project statistics
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
        total_on_hold_tasks=total_on_hold_tasks,
        total_overdue_tasks=total_overdue_tasks,
    )
#==================================================get the health of a project==========================
    @staticmethod
    def get_project_health(
        db: Session, 
        project_id: int) -> ProjectHealth:
        """
        Get project health indicators.
        """

        # we need to first check wether the current user is a member of the project and also find a project assigned to the project we are trying to look for depending on their id
        #member = get_current_project_member(project_id)

        #then we also need to check if the project exists at all
        project = db.query(Project).filter(Project.id == project_id).first()

        if not project:
            raise HTTPException(status_code=404, detail="This Project does not exist")


        
       
        #to get a project health we will use these 4 indicators:
        #1. we check for overdues tasks
        overdue_tasks = db.query(Task).filter(Task.project_id == project_id, Task.status == "overdue").all()
        overdue_count = len(overdue_tasks)
        overdue_indicator = ProjectHealthIndicator(
            status=HealthFlag.alert if overdue_count > 0 else HealthFlag.ok,
            message=f"{overdue_count} overdue tasks"
        )
    
        # 2. the seond is that we will have to check for inactive members that have no logged hours in the last N days
        #we will use the last 7 days as the threshold
        threshold_date = datetime.now() - timedelta(days=7)
        last_n_days = 7
        # Get all project members
        members = db.query(ProjectMember).filter(ProjectMember.project_id == project_id).all()
        inactive_members_list = []
        
        for member in members:
            # Check for logged hours in last N days
            recent_log = db.query(LoggedHour).filter(
                LoggedHour.project_id == project_id,
                LoggedHour.user_id == member.user_id,
                LoggedHour.date >= threshold_date
            ).first()
            
            if not recent_log:
                user = db.query(User).filter(User.id == member.user_id).first()
                if user:
                    inactive_members_list.append({"id": user.id, "name": f"{user.first_name} {user.last_name}"})
        
        inactive_indicator = ProjectHealthIndicator(
            status=HealthFlag.warning if inactive_members_list else HealthFlag.ok,
            message=f"{len(inactive_members_list)} inactive members in the last {last_n_days} days",
            details={"members": inactive_members_list} if inactive_members_list else None
        )

        # 3. The third is that we will check for tasks with no assignee
        unassigned_tasks = db.query(Task).filter(
            Task.project_id == project_id,
            Task.assigned_to == None
        ).all()
        unassigned_count = len(unassigned_tasks)
        unassigned_details = [{"id": t.id, "title": t.title} for t in unassigned_tasks]
        
        unassigned_indicator = ProjectHealthIndicator(
            status=HealthFlag.info if unassigned_count > 0 else HealthFlag.ok,
            message=f"{unassigned_count} tasks with no assignees",
            details={"tasks": unassigned_details} if unassigned_details else None
        )

        # 5. Activity Drop-off (last month vs previous month)
        # We compare count of completed tasks or updated tasks. Let's use tasks completed.
        last_month_start = now() - timedelta(days=30)
        prev_month_start = now() - timedelta(days=60)
        
        last_month_activity = db.query(Task).filter(
            Task.project_id == project_id,
            Task.status == "completed",
            Task.updated_at >= last_month_start
        ).count()
        
        prev_month_activity = db.query(Task).filter(
            Task.project_id == project_id,
            Task.status == "completed",
            Task.updated_at >= prev_month_start,
            Task.updated_at < last_month_start
        ).count()
        
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
                "previous_month_count": prev_month_activity
            }
        )

        return ProjectHealth(
            project_id=project_id,
            overdue_tasks=overdue_indicator,
            inactive_members=inactive_indicator,
            unassigned_tasks=unassigned_indicator,
            activity_dropoff=activity_indicator
        )

        


