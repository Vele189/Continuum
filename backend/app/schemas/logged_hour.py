from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class LoggedHourBase(BaseModel):
    """Base schema for logged hours"""

    task_id: Optional[int] = None
    project_id: int  # Always required (non-nullable)
    hours: Decimal
    description: str
    date: datetime


class LoggedHourResponse(BaseModel):
    """Response schema for logged hours - maps model fields to API fields"""

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: int
    user_id: int
    task_id: Optional[int] = None
    project_id: int
    hours: float
    description: Optional[str] = Field(None, validation_alias="note")
    date: Optional[datetime] = Field(None, validation_alias="logged_at")
    created_at: Optional[datetime] = Field(None, validation_alias="logged_at")
    updated_at: Optional[datetime] = None


class LoggedHourCreate(LoggedHourBase):
    """Schema for creating a logged hour entry"""

    @model_validator(mode="after")
    def validate_task_or_project(self):
        """Validate that project_id is provided (task_id is optional)"""
        if self.project_id is None:
            raise ValueError("project_id is required")
        return self

    @field_validator("hours")
    @classmethod
    def validate_hours(cls, v):
        """Validate that hours is greater than 0"""
        if v is not None:
            hours_float = float(v)
            if hours_float <= 0:
                raise ValueError("hours must be greater than 0")
        return v


class LoggedHourUpdate(BaseModel):
    """Schema for updating a logged hour entry"""

    task_id: Optional[int] = None
    project_id: Optional[int] = None
    hours: Optional[Decimal] = None
    description: Optional[str] = None
    date: Optional[datetime] = None

    @model_validator(mode="after")
    def validate_task_or_project(self):
        """Validate that if both task_id and project_id are provided"""
        if self.task_id is None and self.project_id is None:
            # If updating, it's okay to not provide either if other fields are updated
            pass
        return self

    @field_validator("hours")
    @classmethod
    def validate_hours(cls, v):
        """Validate that hours is greater than 0 if provided"""
        if v is not None:
            hours_float = float(v)
            if hours_float <= 0:
                raise ValueError("hours must be greater than 0")
        return v


class LoggedHour(LoggedHourBase):
    """Schema for logged hour response"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None


class LoggedHourWithTaskAndProject(LoggedHour):
    """Schema for logged hour with task and project details"""

    model_config = ConfigDict(from_attributes=True)

    # These will be populated from relationships
    task: Optional[dict] = None
    project: Optional[dict] = None
