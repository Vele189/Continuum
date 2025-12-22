from typing import Optional, List
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, ConfigDict

from app.schemas.client import Client
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
    updated_at: datetime


class Project(ProjectInDBBase):
    pass


class ProjectWithClient(Project):
    client: Optional[Client] = None


class ProjectMemberBase(BaseModel):
    user_id: int
    role: str = "member"


class ProjectMemberCreate(ProjectMemberBase):
    pass


class ProjectMember(ProjectMemberBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    added_at: datetime
    user: Optional[User] = None


class ProjectWithMembers(Project):
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
    updated_at: datetime


class ProjectDetail(ProjectWithMembers):
    tasks: List[TaskSummary] = []
    total_logged_hours: float = 0.0
