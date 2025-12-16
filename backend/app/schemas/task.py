from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from .project import Project

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "To Do"
    assigned_to: Optional[int] = None

class TaskCreate(TaskBase):
    project_id: int

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    assigned_to: Optional[int] = None

class Task(TaskBase):
    id: int
    project_id: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True

class TaskWithProject(Task):
    project: Optional[Project] = None
    # aggregated_logged_hours could be a computed field or added later if specific time log schema exists
