from datetime import datetime
from enum import Enum
from typing import List, Optional

from app.schemas.task import Task
from pydantic import BaseModel, ConfigDict


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
    # Note: Description wasn't in DB model
    description: Optional[str] = None


class MilestoneCreate(MilestoneBase):
    project_id: int


class MilestoneUpdate(BaseModel):
    name: Optional[str] = None
    due_date: Optional[datetime] = None
    # Status is automatic, updates automatically


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
