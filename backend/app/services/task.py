from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.dbmodels import Task, Project, User, ProjectMember
from app.schemas.task import TaskCreate, TaskUpdate


def validate_project_membership(db: Session, project_id: int, user_id: int) -> bool:
    """
    Validate if a user is a member of a project.

    Returns True if the user is a member of the project, False otherwise.
    """
    member = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == user_id
    ).first()
    return member is not None


def get(db: Session, task_id: int) -> Optional[Task]:
    """Get a task by ID."""
    return db.query(Task).filter(Task.id == task_id).first()


def get_multi(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    project_id: Optional[int] = None,
    status: Optional[str] = None,
    assigned_to: Optional[int] = None
) -> List[Task]:
    """Get multiple tasks with optional filters."""
    query = db.query(Task)
    if project_id:
        query = query.filter(Task.project_id == project_id)
    if status:
        query = query.filter(Task.status == status)
    if assigned_to:
        query = query.filter(Task.assigned_to == assigned_to)
    return query.offset(skip).limit(limit).all()


def create(db: Session, obj_in: TaskCreate) -> Task:
    """Create a new task."""
    # Validate Project exists
    project = db.query(Project).filter(Project.id == obj_in.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    db_obj = Task(
        title=obj_in.title,
        description=obj_in.description,
        status=obj_in.status,
        project_id=obj_in.project_id,
        assigned_to=obj_in.assigned_to,
        due_date=obj_in.due_date
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update(db: Session, db_obj: Task, obj_in: TaskUpdate) -> Task:
    """Update a task."""
    update_data = obj_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_status(db: Session, task_id: int, new_status: str) -> Task:
    """Update only the status of a task."""
    task = get(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.status = new_status
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def delete(db: Session, task_id: int) -> Optional[Task]:
    """Delete a task."""
    obj = db.query(Task).filter(Task.id == task_id).first()
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return obj


def assign(db: Session, task_id: int, user_id: Optional[int]) -> Task:
    """Assign a task to a user."""
    task = get(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if user_id:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        # Validate user is member of the task's project
        if not validate_project_membership(db, task.project_id, user_id):
            raise HTTPException(
                status_code=403,
                detail="User is not a member of this project"
            )

    task.assigned_to = user_id
    db.add(task)
    db.commit()
    db.refresh(task)
    return task
