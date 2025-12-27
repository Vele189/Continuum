from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class TaskSummary(BaseModel):
    id: int
    title: str
    status: str
    completed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class UserHours(BaseModel):
    user_id: int
    user_name: str
    hours: float


class CommitSummary(BaseModel):
    hash: str
    message: Optional[str] = None
    author_name: str
    created_at: datetime


class RiskItem(BaseModel):
    reason: str
    severity: str  # "info", "warning", "alert"


class WeeklyDigest(BaseModel):
    project_id: int
    project_name: str
    week_start: datetime
    week_end: datetime
    completed_tasks: List[TaskSummary]
    total_hours_logged: float
    hours_breakdown: List[UserHours]
    commits: List[CommitSummary]
    milestone_progress: Optional[dict] = None
    risks_and_delays: List[RiskItem] = []

    model_config = ConfigDict(from_attributes=True)
