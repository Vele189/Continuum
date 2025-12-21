from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict, field_validator


class GitContributionBase(BaseModel):
    """Base schema for git contributions."""
    project_id: int
    task_id: Optional[int] = None
    commit_hash: str
    branch: Optional[str] = None
    commit_message: Optional[str] = None
    provider: str
    commit_url: Optional[str] = None


class GitContributionCreate(GitContributionBase):
    """Schema for creating a git contribution."""
    user_id: int

    @field_validator('commit_hash')
    @classmethod
    def validate_commit_hash(cls, v):
        """Validate that commit_hash is provided and not empty."""
        if not v or not v.strip():
            raise ValueError('commit_hash is required')
        return v.strip()

    @field_validator('project_id')
    @classmethod
    def validate_project_id(cls, v):
        """Validate that project_id is provided."""
        if v is None:
            raise ValueError('project_id is required')
        return v

    @field_validator('provider')
    @classmethod
    def validate_provider(cls, v):
        """Validate that provider is provided."""
        if not v or not v.strip():
            raise ValueError('provider is required')
        return v.strip().lower()


class GitContributionUpdate(BaseModel):
    """Schema for updating a git contribution."""
    task_id: Optional[int] = None
    commit_message: Optional[str] = None
    commit_url: Optional[str] = None


class GitContribution(GitContributionBase):
    """Full git contribution response schema."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    created_at: datetime
