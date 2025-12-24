from typing import Optional, List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import ProjectMember

from app.api import deps
from app.dbmodels import User
from app.schemas.logged_hour import (
    LoggedHourCreate,
    LoggedHourUpdate,
    LoggedHour
)
from app.services import logged_hour as logged_hour_service

router = APIRouter()


@router.post("/", response_model=LoggedHour, status_code=status.HTTP_201_CREATED)
def create_logged_hour(
    logged_hour_in: LoggedHourCreate,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    """
    Log work hours.

    - **Authentication required**
    - Users can only log their own hours
    - Users can only log hours to tasks they are assigned to OR projects they are a member of
    - Non-members attempting to log hours → 403 Forbidden
    """
    return logged_hour_service.create(db, obj_in=logged_hour_in, user_id=current_user.id)


@router.get("/", response_model=List[LoggedHour])
def list_logged_hours(
    user_id: Optional[int] = Query(None, description="Filter by user ID"),
    task_id: Optional[int] = Query(None, description="Filter by task ID"),
    project_id: Optional[int] = Query(None, description="Filter by project ID"),
    start_date: Optional[datetime] = Query(None, description="Filter by start date (inclusive)"),
    end_date: Optional[datetime] = Query(None, description="Filter by end date (inclusive)"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    """
    List logged hours (filterable).

    - **Authentication required**
    - Users can only see their own entries (unless admin)
    - Admins can see all entries
    - Filters are composable (can be combined)
    - Supported filters: user_id, task_id, project_id, start_date, end_date
    """
    return logged_hour_service.list_logged_hours(
        db=db,
        current_user=current_user,
        user_id=user_id,
        task_id=task_id,
        project_id=project_id,
        start_date=start_date,
        end_date=end_date,
        skip=skip,
        limit=limit
    )


@router.get("/{logged_hour_id}", response_model=LoggedHour)
def get_logged_hour(
    logged_hour_id: int,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    """
    Get logged hour details.

    - **Authentication required**
    - **Access**: Owner / Admin
    - Users can only view their own entries
    - Admins can view all entries
    """
    logged_hour = logged_hour_service.get_by_id(
        db, logged_hour_id=logged_hour_id, current_user=current_user
    )
    if not logged_hour:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Logged hour entry not found"
        )
    return logged_hour


@router.put("/{logged_hour_id}", response_model=LoggedHour)
def update_logged_hour(
    logged_hour_id: int,
    logged_hour_in: LoggedHourUpdate,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    """
    Update logged hour.

    - **Authentication required**
    - **Access**: Owner only
    - Users can only modify their own entries
    """
    return logged_hour_service.update(
        db=db,
        logged_hour_id=logged_hour_id,
        obj_in=logged_hour_in,
        current_user=current_user
    )


@router.delete("/{logged_hour_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_logged_hour(
    logged_hour_id: int,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    """
    Delete logged hour.

    - **Authentication required**
    - **Access**: Owner / Admin
    - Users can delete their own entries
    - Admins can delete any entry
    """
    logged_hour_service.delete(
        db=db, logged_hour_id=logged_hour_id, current_user=current_user
    )


# Aggregation endpoints - these will be registered separately in main.py
aggregation_router = APIRouter()


@aggregation_router.get("/tasks/{task_id}/hours")
def get_task_hours(
    task_id: int,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    """
    Get all hours for a task.

    - **Authentication required**
    - Returns total hours and optional breakdown per user
    - Users can view hours for tasks they are assigned to
    - or projects they are members of
    - Admins can view all task hours
    """
    return logged_hour_service.get_total_hours_for_task(
        db=db,
        task_id=task_id,
        current_user=current_user
    )


@aggregation_router.get("/projects/{project_id}/hours")
def get_project_hours(
    project_id: int,
    db: Session = Depends(deps.get_db),
    member: ProjectMember = Depends(deps.get_current_project_member),
):
    """
    Get all hours for a project.

    - **Authentication required**
    - Returns total hours and breakdown per user
    - Users can view hours for projects they are members of
    - Admins can view all project hours
    """
    return logged_hour_service.get_total_hours_for_project(
        db=db,
        project_id=project_id,
        current_user=member.user # Use user from member record
    )
