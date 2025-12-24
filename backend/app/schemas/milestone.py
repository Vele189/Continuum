from typing import Optional, List
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, ConfigDict
from app.schemas.task import Task

class MilestoneStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    OVERDUE = "overdue"

class MilestoneProgress(BaseModel):
    total_tasks: int
    completed_tasks: int
    in_progress_tasks: int
    todo_tasks: int
    completion_percentage: float

class MilestoneBase(BaseModel):
    name: str
    due_date: Optional[datetime] = None
    description: Optional[str] = None # Note: Description wasn't in DB model, checking if I missed it. 
    # Logic check: User didn't specify description in DB scope but often used. 
    # Scope says: "Has a due date, Tracks status automatically". 
    # "Milestone Entity" scope doesn't explicitly mention description. I'll omit it for now to match DB.

class MilestoneCreate(MilestoneBase):
    project_id: int

class MilestoneUpdate(BaseModel):
    name: Optional[str] = None
    due_date: Optional[datetime] = None
    # Status is automatic, but usually we might want to override? 
    # Scope says: "Status must update automatically". 
    # So I will NOT allow manual status update in this schema unless needed.
    # However, sometimes manual override is needed. I'll stick to auto for now.

class MilestoneInDBBase(MilestoneBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    project_id: int
    status: MilestoneStatus
    created_at: datetime
    updated_at: Optional[datetime] = None

class Milestone(MilestoneInDBBase):
    progress: Optional[MilestoneProgress] = None
    tasks: List[Task] = []
