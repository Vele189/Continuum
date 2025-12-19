from pydantic import BaseModel, field_validator
from typing import Optional, List, Literal
from datetime import datetime
from .project import Project

# Allowed status values
ALLOWED_STATUSES = ["todo", "in_progress", "done"]

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Literal["todo", "in_progress", "done"] = "todo"
    assigned_to: Optional[int] = None

class TaskCreate(TaskBase):
    project_id: int

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[Literal["todo", "in_progress", "done"]] = None
    assigned_to: Optional[int] = None

class Task(TaskBase):
    id: int
    project_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class TaskWithProject(Task):
    project: Optional[Project] = None

# Request schemas for specific endpoints
class AssignTaskRequest(BaseModel):
    user_id: Optional[int] = None

class UpdateStatusRequest(BaseModel):
    status: Literal["todo", "in_progress", "done"]
