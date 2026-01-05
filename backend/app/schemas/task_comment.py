from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class TaskCommentAuthor(BaseModel):
    """Basic user info for comment author."""

    id: Optional[int] = None
    display_name: Optional[str] = None
    username: Optional[str] = None

    class Config:
        from_attributes = True


class TaskCommentBase(BaseModel):
    """Base schema for task comments."""

    content: str = Field(..., min_length=1, max_length=5000)


class TaskCommentCreate(TaskCommentBase):
    """Schema for creating a new comment."""


class TaskCommentUpdate(BaseModel):
    """Schema for updating a comment."""

    content: str = Field(..., min_length=1, max_length=5000)


class TaskComment(TaskCommentBase):
    """Schema for comment response."""

    id: int
    task_id: int
    user_id: Optional[int] = None
    author: Optional[TaskCommentAuthor] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
