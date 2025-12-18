from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api import deps
from app.models.user import User, UserRole
from app.schemas.task import Task, TaskCreate, TaskUpdate, AssignTaskRequest, UpdateStatusRequest
from app.services import task as task_service

router = APIRouter()

@router.post("/", response_model=Task)
def create_task(
    task_in: TaskCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    # Verify project membership
    print(f"DEBUG: Validating membership - project_id={task_in.project_id}, user_id={current_user.id}")
    is_member = task_service.validate_project_membership(db, task_in.project_id, current_user.id)
    print(f"DEBUG: Membership result = {is_member}")
    if not is_member:
        raise HTTPException(status_code=403, detail="Not a member of this project")
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
    # TODO: Filter by projects user is member of
    return task_service.get_multi(
        db, skip=skip, limit=limit, project_id=project_id, status=status, assigned_to=assigned_to
    )

@router.get("/{task_id}", response_model=Task)
def get_task(
    task_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    task = task_service.get(db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    # Verify project membership
    if not task_service.validate_project_membership(db, task.project_id, current_user.id):
        raise HTTPException(status_code=403, detail="Not a member of this project")
    return task

@router.put("/{task_id}", response_model=Task)
def update_task(
    task_id: int,
    task_in: TaskUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    task = task_service.get(db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    # Verify project membership
    if not task_service.validate_project_membership(db, task.project_id, current_user.id):
        raise HTTPException(status_code=403, detail="Not a member of this project")
    task = task_service.update(db, db_obj=task, obj_in=task_in)
    return task

@router.delete("/{task_id}", response_model=Task)
def delete_task(
    task_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    # Admin check (Assuming PROJECTMANAGER is Admin)
    # The requirement said "Admins may delete any task".
    # print(f"DEBUG: User Role: {current_user.role} (Type: {type(current_user.role)})")
    if current_user.role.value != UserRole.PROJECTMANAGER.value and current_user.role.value != UserRole.CLIENT.value:
         raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    
    task = task_service.get(db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = task_service.delete(db, task_id=task_id)
    return task

@router.patch("/{task_id}/status", response_model=Task)
def update_task_status(
    task_id: int,
    status_update: UpdateStatusRequest,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    task = task_service.get(db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    # Verify project membership
    if not task_service.validate_project_membership(db, task.project_id, current_user.id):
        raise HTTPException(status_code=403, detail="Not a member of this project")
    
    return task_service.update_status(db, task_id=task_id, new_status=status_update.status)

@router.patch("/{task_id}/assign", response_model=Task)
def assign_task(
    task_id: int,
    assign_request: AssignTaskRequest,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    task = task_service.get(db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    # Verify project membership
    if not task_service.validate_project_membership(db, task.project_id, current_user.id):
        raise HTTPException(status_code=403, detail="Not a member of this project")
    
    task = task_service.assign(db, task_id=task_id, user_id=assign_request.user_id)
    return task
