# User model
from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime, Enum
from sqlalchemy.sql import func
import enum
from app.db.base import Base

class UserRole(enum.Enum):
    BACKEND = "backend"
    FRONTEND = "frontend"
    DESIGNER = "designer"
    CLIENT = "client"
    PROJECTMANAGER = "project_manager"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    role = Column(Enum(UserRole), default=UserRole.FRONTEND)
    hourly_rate = Column(Numeric(10,2))

    #email ver
    is_verified = Column(Boolean, default=False)
    verification_token = Column(String(255))
    refresh_token = Column(String(255), nullable=True)
    password_reset_token = Column(String(255), nullable=True)