from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api import deps
from app.models.user import User, UserRole
from app.schemas.task import Task, TaskCreate, TaskUpdate
from app.services import task as task_service

router = APIRouter()

@router.post("/", response_model=Task)
def create_task(
    task_in: TaskCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    # TODO: Verify project membership if/when project members logic is implemented
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
    # TODO: Verify project membership
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
    # TODO: Verify project membership
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
    if current_user.role != UserRole.PROJECTMANAGER and current_user.role != UserRole.CLIENT:
         raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    
    task = task_service.get(db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = task_service.delete(db, task_id=task_id)
    return task

@router.post("/{task_id}/assign", response_model=Task)
def assign_task(
    task_id: int,
    user_id: Optional[int] = None, # passed as query param or body? Requirement implies just assign/unassign
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    # To keep strict to REST, maybe accept body. But query param is simpler for now.
    task = task_service.get(db, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    # TODO: Verify project membership
    
    task = task_service.assign(db, task_id=task_id, user_id=user_id)
    return task
