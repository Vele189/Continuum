from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import HTTPException, status
from app.models.task import Task
from app.models.project import Project
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate

def get(db: Session, task_id: int) -> Optional[Task]:
    return db.query(Task).filter(Task.id == task_id).first()

def get_multi(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    project_id: Optional[int] = None, 
    status: Optional[str] = None, 
    assigned_to: Optional[int] = None
) -> List[Task]:
    query = db.query(Task)
    if project_id:
        query = query.filter(Task.project_id == project_id)
    if status:
        query = query.filter(Task.status == status)
    if assigned_to:
        query = query.filter(Task.assigned_to == assigned_to)
    return query.offset(skip).limit(limit).all()

def create(db: Session, obj_in: TaskCreate) -> Task:
    # Validate Project
    project = db.query(Project).filter(Project.id == obj_in.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    db_obj = Task(
        title=obj_in.title,
        description=obj_in.description,
        status=obj_in.status,
        project_id=obj_in.project_id,
        assigned_to=obj_in.assigned_to
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update(db: Session, db_obj: Task, obj_in: TaskUpdate) -> Task:
    update_data = obj_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete(db: Session, task_id: int) -> Task:
    obj = db.query(Task).filter(Task.id == task_id).first()
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj

def assign(db: Session, task_id: int, user_id: Optional[int]) -> Task:
    task = get(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if user_id:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        # Optional: Validate user is member of project (requires Project Members model/table)
        # For now, we skip this check as we don't have the ProjectMembers model loaded/created yet
    
    task.assigned_to = user_id
    db.add(task)
    db.commit()
    db.refresh(task)
    return task
