# User model
from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime, Enum
from sqlalchemy.sql import func
import enum
from app.db.base import Base

class UserRole(enum.Enum):
    BACKEND = "backend"
    FRONTEND = "frontend"
    FULLSTACK = "fullstack"
    CLIENT = "client"
    PROJECTMANAGER = "project_manager"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    role = Column(Enum(UserRole), default=UserRole.FRONTEND)
    hourly_rate = Column(Numeric(10,2))

    #email ver
    is_verified = Column(Boolean, default=False)
    verification_token = Column(String)