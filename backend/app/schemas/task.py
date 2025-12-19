from pydantic import BaseModel, field_validator, ConfigDict
from typing import Optional, List, Literal
from datetime import datetime
from .project import Project

# Allowed status values
ALLOWED_STATUSES = ["todo", "in_progress", "done"]

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Literal["todo", "in_progress", "done"] = "todo"
    project_id: int
    assigned_to: Optional[int] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[Literal["todo", "in_progress", "done"]] = None
    assigned_to: Optional[int] = None

class TaskInDBBase(TaskBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime

class Task(TaskInDBBase):
    pass

class TaskWithProject(Task):
    project: Optional[Project] = None

# Request schemas for specific endpoints
class AssignTaskRequest(BaseModel):
    user_id: Optional[int] = None

class UpdateStatusRequest(BaseModel):
    status: Literal["todo", "in_progress", "done"]
