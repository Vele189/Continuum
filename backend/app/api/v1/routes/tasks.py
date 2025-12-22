# pylint: disable=unused-argument,redefined-outer-name
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.api.deps import (
    is_admin_user, 
    get_current_project_member,
    get_current_project_admin
)
from app.database import User, ProjectMember
from app.schemas.task import Task, TaskCreate, TaskUpdate, AssignTaskRequest, UpdateStatusRequest
from app.services import task as task_service

router = APIRouter()


@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(
    task_in: TaskCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Create a new task.

    Requires the user to be a member of the project.
    """
    # Verify project membership (admins bypass this check)
    if not is_admin_user(current_user):
        # This will raise 403 if not a member
        get_current_project_member(
            project_id=task_in.project_id,
            current_user=current_user,
            db=db
        )

    return task_service.create(db, obj_in=task_in)


@router.get("/", response_model=List[Task])
def list_tasks(
    skip: int = 0,
    limit: int = 100,
    project_id: Optional[int] = None,
    status: Optional[str] = None,
    assigned_to: Optional[int] = None,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    List tasks with optional filters.

    - Admins see all tasks
    - Regular users see only tasks from projects they are members of
    """
    tasks = task_service.get_multi(
        db, skip=skip, limit=limit, project_id=project_id, status=status, assigned_to=assigned_to
    )

    # Admins see all tasks
    if is_admin_user(current_user):
        return tasks

    # Filter tasks to only include those from projects the user is a member of
    filtered_tasks = []
    for task in tasks:
        try:
            get_current_project_member(
                project_id=task.project_id,
                current_user=current_user,
                db=db
            )
            filtered_tasks.append(task)
        except HTTPException:
            # User is not a member of this project, skip it
            continue

    return filtered_tasks


@router.get("/{task_id}", response_model=Task)
def get_task(
    task_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Get a task by ID.

    Requires the user to be a member of the project (or admin).
    """
    task = task_service.get(db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Verify project membership (admins bypass)
    if not is_admin_user(current_user):
        get_current_project_member(
            project_id=task.project_id,
            current_user=current_user,
            db=db
        )

    return task


@router.put("/{task_id}", response_model=Task)
def update_task(
    task_id: int,
    task_in: TaskUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Update a task.

    Requires the user to be a member of the project (or admin).
    """
    task = task_service.get(db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Verify project membership (admins bypass)
    if not is_admin_user(current_user):
        get_current_project_member(
            project_id=task.project_id,
            current_user=current_user,
            db=db
        )

    return task_service.update(db, db_obj=task, obj_in=task_in)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Delete a task.

    Requires admin privileges (ADMIN or PROJECTMANAGER role).
    """
    task = task_service.get(db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Verify project admin privileges (will raise 403 if not admin)
    get_current_project_admin(
        project_id=task.project_id,
        current_user=current_user,
        db=db
    )

    task_service.delete(db, task_id=task_id)


@router.patch("/{task_id}/status", response_model=Task)
def update_task_status(
    task_id: int,
    status_update: UpdateStatusRequest,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Update only the status of a task.

    Requires the user to be a member of the project (or admin).
    """
    task = task_service.get(db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Verify project membership (admins bypass)
    if not is_admin_user(current_user):
        get_current_project_member(
            project_id=task.project_id,
            current_user=current_user,
            db=db
        )

    return task_service.update_status(db, task_id=task_id, new_status=status_update.status)


@router.patch("/{task_id}/assign", response_model=Task)
def assign_task(
    task_id: int,
    assign_request: AssignTaskRequest,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Assign a task to a user.

    Requires project admin privileges (ADMIN or PROJECTMANAGER role).
    """
    task = task_service.get(db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Verify project admin privileges (will raise 403 if not admin)
    get_current_project_admin(
        project_id=task.project_id,
        current_user=current_user,
        db=db
    )

    return task_service.assign(db, task_id=task_id, user_id=assign_request.user_id)