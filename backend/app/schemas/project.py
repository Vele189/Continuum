from decimal import Decimal
from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from app.schemas.client import Client
from app.schemas.task import Task
from app.schemas.user import User

class ProjectStatus(str, Enum):
    active = "active"
    completed = "completed"
    on_hold = "on_hold"


class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: str = "active"
    client_id: int


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    client_id: Optional[int] = None


class ProjectInDBBase(ProjectBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None


class Project(ProjectInDBBase):
    pass


class ProjectWithClient(Project):
    client: Optional[Client] = None


class ProjectMemberBase(BaseModel):
    user_id: int
    role: str = "member"



class ProjectMemberCreate(ProjectMemberBase):
    pass

class TaskCount(BaseModel):
    """Schema for task statistics and logged hours of a project member."""
    hours_logged: Decimal = 0.0
    tasks_count: int = 0
    completed_tasks_count: int = 0
    in_progress_tasks_count: int = 0
    todo_tasks_count: int = 0
    overdue_tasks_count: int = 0

class ProjectMember(ProjectMemberBase):
    """Schema for a project member, including user details and optional task statistics."""
    model_config = ConfigDict(from_attributes=True)
    id: int
    added_at: datetime
    user: Optional[User] = None
    task_count: Optional[TaskCount] = None



class ProjectWithMembers(Project):
    """Schema for a project including its list of members."""
    members: List[ProjectMember] = []



# Simplified Task schema for ProjectDetail to avoid circular import
class TaskSummary(BaseModel):
    """Simplified task for embedding in project details"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: Optional[str] = None
    status: str
    assigned_to: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None



class ProjectDetail(ProjectWithMembers):
    """Detailed project schema including tasks and total logged hours."""
    tasks: List[Task] = []
    total_logged_hours: float = 0.0


# This is the project statistics schema
class ProjectStatistics(ProjectDetail):
    """Schema for comprehensive project statistics."""
    total_logged_hours: float = 0.0
    total_tasks: int = 0
    total_completed_tasks: int = 0
    total_in_progress_tasks: int = 0
    total_todo_tasks: int = 0
    total_overdue_tasks: int = 0

class HealthFlag(str, Enum):
    ok = "ok"
    info = "info"
    warning = "warning"
    alert = "alert"

class ProjectHealthIndicator(BaseModel):
    """Schema for an individual health indicator."""
    status: HealthFlag
    message: str
    details: Optional[dict] = None

class ProjectHealth(BaseModel):
    """Schema for overall project health."""
    project_id: int
    overdue_tasks: ProjectHealthIndicator
    inactive_members: ProjectHealthIndicator
    unassigned_tasks: ProjectHealthIndicator
    activity_dropoff: ProjectHealthIndicator

