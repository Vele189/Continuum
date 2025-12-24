from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class AttachmentUploader(BaseModel):
    """Basic user info for attachment uploader"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    first_name: str
    last_name: str
    display_name: Optional[str] = None


class TaskAttachmentBase(BaseModel):
    """Base schema for task attachments"""
    original_filename: str
    file_size: int
    mime_type: str


class TaskAttachmentCreate(TaskAttachmentBase):
    """Schema for creating a task attachment (internal use)"""
    task_id: int
    user_id: int
    filename: str
    file_path: str


class TaskAttachmentInDBBase(TaskAttachmentBase):
    """Base schema with database fields"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    filename: str
    file_path: str
    created_at: datetime
    updated_at: Optional[datetime] = None


class TaskAttachment(TaskAttachmentInDBBase):
    """Full task attachment response with uploader info"""
    uploader: AttachmentUploader


class TaskAttachmentList(BaseModel):
    """List of task attachments"""
    attachments: list[TaskAttachment]
    total: int
