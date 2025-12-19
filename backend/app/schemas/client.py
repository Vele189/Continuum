from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict, field_validator


class ClientBase(BaseModel):
    """Base schema with shared properties"""
    name: str
    email: Optional[EmailStr] = None


class ClientCreate(ClientBase):
    """Schema for creating a new client"""
    name: str
    email: Optional[EmailStr] = None

    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        """Validate that name is not empty"""
        if not v or not v.strip():
            raise ValueError('name cannot be empty')
        return v.strip()


class ClientUpdate(BaseModel):
    """Schema for updating a client"""
    name: Optional[str] = None
    email: Optional[EmailStr] = None

    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        """Validate that name is not empty if provided"""
        if v is not None and (not v or not v.strip()):
            raise ValueError('name cannot be empty')
        return v.strip() if v else v


class ClientInDBBase(ClientBase):
    """Base schema for database representation"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_by: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None


class Client(ClientInDBBase):
    """Full client response model"""
    id: int
    name: str
    email: Optional[str] = None
    created_by: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
