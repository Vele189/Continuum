from typing import Optional
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, EmailStr, field_validator, ConfigDict
from app.database import UserRole

# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    first_name: str
    last_name: str
    role: Optional[UserRole] = UserRole.FRONTEND

# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None

class UserInDBBase(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None

class User(UserInDBBase):
    """Full user response with all public fields"""
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    role: UserRole
    hourly_rate: Decimal
    display_name: str
    is_verified: bool
    created_at: datetime

class UserInDB(UserInDBBase):
    hashed_password: str

# Login schemas
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str

class TokenPayload(BaseModel):
    model_config = ConfigDict(extra='ignore')

    sub: Optional[int] = None

    @field_validator('sub', mode='before')
    @classmethod
    def convert_sub_to_int(cls, v):
        """Allow sub to be string or int, convert string to int"""
        if v is None:
            return None
        if isinstance(v, str):
            try:
                return int(v)
            except ValueError:
                return v
        return v

# Password Reset Schemas
class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str
