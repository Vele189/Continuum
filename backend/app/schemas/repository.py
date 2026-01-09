from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class GitProvider(str, Enum):
    """Supported Git providers for repository webhooks."""

    GITHUB = "github"
    GITLAB = "gitlab"
    BITBUCKET = "bitbucket"


class RepositoryBase(BaseModel):
    repository_url: str
    repository_name: str
    provider: GitProvider
    is_active: bool = True


class RepositoryCreate(RepositoryBase):
    project_id: int
    webhook_secret: Optional[str] = None


class RepositoryUpdate(BaseModel):
    is_active: Optional[bool] = None
    webhook_secret: Optional[str] = None


class RepositoryOut(RepositoryBase):
    id: int
    project_id: int
    webhook_secret: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
