from typing import Optional, Literal
from datetime import datetime
from pydantic import BaseModel, ConfigDict

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


# Request schemas for specific endpoints
class AssignTaskRequest(BaseModel):
    user_id: Optional[int] = None


class UpdateStatusRequest(BaseModel):
    status: Literal["todo", "in_progress", "done"]
