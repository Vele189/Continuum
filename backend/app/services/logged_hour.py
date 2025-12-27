from datetime import datetime
from typing import List, Optional

from app.dbmodels import LoggedHour, Project, ProjectMember, Task, User, UserRole
from app.schemas.logged_hour import LoggedHourCreate, LoggedHourUpdate
from fastapi import HTTPException, status
from sqlalchemy import and_
from sqlalchemy.orm import Session


def _is_admin(user: User) -> bool:
    """Check if user has admin privileges."""
    return user.role in {UserRole.ADMIN, UserRole.PROJECTMANAGER}


def create(db: Session, obj_in: LoggedHourCreate, user_id: int) -> LoggedHour:
    """
    Create a new logged hour entry.

    Business Rules:
    - User can only log hours to tasks they are assigned to OR projects they are a member of
    - If task_id is provided, verify user is assigned to the task
    - If only project_id is provided, verify user is a member of the project
    """
    # Validate task assignment or project membership
    if obj_in.task_id:
        # Check if task exists and user is assigned to it
        task = db.query(Task).filter(Task.id == obj_in.task_id).first()
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

        # Verify task belongs to the specified project
        if task.project_id != obj_in.project_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Task does not belong to the specified project",
            )

        # Check if user is assigned to the task
        if task.assigned_to != user_id:
            # Also check if user is a project member
            # (they can log hours even if not directly assigned)
            is_member = (
                db.query(ProjectMember)
                .filter(
                    and_(
                        ProjectMember.project_id == obj_in.project_id,
                        ProjectMember.user_id == user_id,
                    )
                )
                .first()
            )
            if not is_member:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You are not assigned to this task or a member of this project",
                )
    else:
        # Only project_id provided - check if user is a project member
        is_member = (
            db.query(ProjectMember)
            .filter(
                and_(
                    ProjectMember.project_id == obj_in.project_id, ProjectMember.user_id == user_id
                )
            )
            .first()
        )
        if not is_member:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="You are not a member of this project"
            )

    # Verify project exists
    project = db.query(Project).filter(Project.id == obj_in.project_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    # Create the logged hour entry
    # Map schema fields to model fields: description -> note, date -> logged_at
    db_obj = LoggedHour(
        user_id=user_id,
        task_id=obj_in.task_id,
        project_id=obj_in.project_id,
        hours=float(obj_in.hours),
        note=obj_in.description,
        logged_at=obj_in.date,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_by_id(db: Session, logged_hour_id: int, current_user: User) -> Optional[LoggedHour]:
    """
    Retrieve a logged hour by ID.

    Business Rules:
    - Owner can view their own entries
    - Admin can view all entries
    """
    logged_hour = db.query(LoggedHour).filter(LoggedHour.id == logged_hour_id).first()

    if not logged_hour:
        return None

    # Check permissions: owner or admin
    is_owner = logged_hour.user_id == current_user.id

    if not (is_owner or _is_admin(current_user)):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to view this logged hour entry",
        )

    return logged_hour


def list_logged_hours(
    db: Session,
    current_user: User,
    user_id: Optional[int] = None,
    task_id: Optional[int] = None,
    project_id: Optional[int] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    skip: int = 0,
    limit: int = 100,
) -> List[LoggedHour]:
    """
    List logged hours with filters.

    Business Rules:
    - Users can only see their own entries (unless admin)
    - Admins can see all entries
    - Filters are composable
    """
    query = db.query(LoggedHour)

    # Permission filter: non-admins can only see their own entries
    is_admin = _is_admin(current_user)
    if not is_admin:
        query = query.filter(LoggedHour.user_id == current_user.id)

    # Apply filters
    if user_id is not None:
        # Admins can filter by any user, non-admins are already filtered to themselves
        if is_admin:
            query = query.filter(LoggedHour.user_id == user_id)

    if task_id is not None:
        query = query.filter(LoggedHour.task_id == task_id)

    if project_id is not None:
        query = query.filter(LoggedHour.project_id == project_id)

    if start_date is not None:
        query = query.filter(LoggedHour.logged_at >= start_date)

    if end_date is not None:
        query = query.filter(LoggedHour.logged_at <= end_date)

    return query.offset(skip).limit(limit).all()


def update(
    db: Session, logged_hour_id: int, obj_in: LoggedHourUpdate, current_user: User
) -> LoggedHour:
    """
    Update a logged hour entry.

    Business Rules:
    - Only the owner can update their entries
    """
    logged_hour = db.query(LoggedHour).filter(LoggedHour.id == logged_hour_id).first()

    if not logged_hour:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Logged hour entry not found"
        )

    # Check if user is the owner
    if logged_hour.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own logged hour entries",
        )

    # Validate task/project if being updated
    if obj_in.task_id is not None or obj_in.project_id is not None:
        new_task_id = obj_in.task_id if obj_in.task_id is not None else logged_hour.task_id
        new_project_id = (
            obj_in.project_id if obj_in.project_id is not None else logged_hour.project_id
        )

        # If task is provided, verify it belongs to the project
        if new_task_id:
            task = db.query(Task).filter(Task.id == new_task_id).first()
            if not task:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
            if task.project_id != new_project_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Task does not belong to the specified project",
                )

        # Verify user still has permission (task assignment or project membership)
        if new_task_id:
            task = db.query(Task).filter(Task.id == new_task_id).first()
            if task.assigned_to != current_user.id:
                is_member = (
                    db.query(ProjectMember)
                    .filter(
                        and_(
                            ProjectMember.project_id == new_project_id,
                            ProjectMember.user_id == current_user.id,
                        )
                    )
                    .first()
                )
                if not is_member:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="You are not assigned to this task or a member of this project",
                    )
        else:
            is_member = (
                db.query(ProjectMember)
                .filter(
                    and_(
                        ProjectMember.project_id == new_project_id,
                        ProjectMember.user_id == current_user.id,
                    )
                )
                .first()
            )
            if not is_member:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You are not a member of this project",
                )

    # Update fields
    update_data = obj_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if field == "hours" and value is not None:
            setattr(logged_hour, field, float(value))
        else:
            setattr(logged_hour, field, value)

    db.add(logged_hour)
    db.commit()
    db.refresh(logged_hour)
    return logged_hour


def delete(db: Session, logged_hour_id: int, current_user: User) -> bool:
    """
    Delete a logged hour entry.

    Business Rules:
    - Owner can delete their own entries
    - Admin can delete any entry
    """
    logged_hour = db.query(LoggedHour).filter(LoggedHour.id == logged_hour_id).first()

    if not logged_hour:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Logged hour entry not found"
        )

    # Check permissions: owner or admin
    is_owner = logged_hour.user_id == current_user.id

    if not (is_owner or _is_admin(current_user)):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this logged hour entry",
        )

    db.delete(logged_hour)
    db.commit()
    return True


def get_total_hours_for_task(db: Session, task_id: int, current_user: User) -> dict:
    """
    Get total hours logged for a specific task.

    Returns:
    - total_hours: Sum of all hours
    - breakdown_per_user: Optional breakdown by user (if admin or task assignee)
    """
    # Verify task exists
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    # Check permissions: user must be assigned to task, project member, or admin
    is_admin = _is_admin(current_user)
    is_assigned = task.assigned_to == current_user.id
    is_member = (
        db.query(ProjectMember)
        .filter(
            and_(
                ProjectMember.project_id == task.project_id,
                ProjectMember.user_id == current_user.id,
            )
        )
        .first()
        is not None
    )

    if not (is_admin or is_assigned or is_member):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to view hours for this task",
        )

    # Get all logged hours for this task
    logged_hours = db.query(LoggedHour).filter(LoggedHour.task_id == task_id).all()

    total_hours = sum(lh.hours for lh in logged_hours)

    # Build breakdown per user (if admin or assigned)
    breakdown_per_user = {}
    if is_admin or is_assigned:
        for lh in logged_hours:
            user_id = lh.user_id
            if user_id not in breakdown_per_user:
                breakdown_per_user[user_id] = {"user_id": user_id, "total_hours": 0.0}
            breakdown_per_user[user_id]["total_hours"] += lh.hours

    return {
        "task_id": task_id,
        "total_hours": total_hours,
        "breakdown_per_user": list(breakdown_per_user.values()) if breakdown_per_user else None,
    }


def get_total_hours_for_project(db: Session, project_id: int, current_user: User) -> dict:
    """
    Get total hours logged for a specific project.

    Returns:
    - total_hours: Sum of all hours
    - breakdown_per_user: Optional breakdown by user (if admin or project member)
    """
    # Verify project exists
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    # Check permissions: user must be project member or admin
    is_admin = _is_admin(current_user)
    is_member = (
        db.query(ProjectMember)
        .filter(
            and_(ProjectMember.project_id == project_id, ProjectMember.user_id == current_user.id)
        )
        .first()
        is not None
    )

    if not (is_admin or is_member):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to view hours for this project",
        )

    # Get all logged hours for this project
    logged_hours = db.query(LoggedHour).filter(LoggedHour.project_id == project_id).all()

    total_hours = sum(lh.hours for lh in logged_hours)

    # Build breakdown per user
    breakdown_per_user = {}
    for lh in logged_hours:
        user_id = lh.user_id
        if user_id not in breakdown_per_user:
            breakdown_per_user[user_id] = {"user_id": user_id, "total_hours": 0.0}
        breakdown_per_user[user_id]["total_hours"] += lh.hours

    return {
        "project_id": project_id,
        "total_hours": total_hours,
        "breakdown_per_user": list(breakdown_per_user.values()),
    }
