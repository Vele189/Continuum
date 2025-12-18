# app/database.py
# pylint: disable=not-callable
import enum
import logging

from sqlalchemy import (
    Boolean,
    Enum,
    Numeric,
    create_engine,
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    DateTime,
    Text,
    JSON,
    UniqueConstraint
)
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from sqlalchemy.sql import func

from app.core.config import settings

# --- Logger Setup ---
try:
    from utils.logger import get_logger
except ImportError:
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s | [%(name)s] %(message)s"
    )

    def get_logger(name: str):
        return logging.getLogger(name)

logger = get_logger(__name__)


# --- Database Configuration ---
DATABASE_URL = settings.DATABASE_URL

# connect_args={"check_same_thread": False} is required for SQLite
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)
# pylint: disable=invalid-name
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class UserRole(enum.Enum):
    BACKEND = "backend"
    FRONTEND = "frontend"
    DESIGNER = "designer"
    CLIENT = "client"
    PROJECTMANAGER = "project_manager"

# --- Models ---

class User(Base):
    __tablename__ = "users"

    # Explicit Primary Key
    id = Column(Integer, primary_key=True, index=True)
    # Unique & Indexed Constraints
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    display_name = Column(String, nullable=False)
    hourly_rate = Column(Numeric(10,2), default=0.0)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.FRONTEND)
    is_verified = Column(Boolean, default=False)
    verification_token = Column(String(255))
    refresh_token = Column(String(255), nullable=True)
    password_reset_token = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    projects_owned = relationship("Client", back_populates="creator")
    tasks_assigned = relationship("Task", back_populates="assignee")
    logged_hours = relationship("LoggedHour", back_populates="user")
    git_contributions = relationship("GitContribution", back_populates="user")
    project_memberships = relationship("ProjectMember", back_populates="user")

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=True, index=True)

    # ADDED: index=True for frequently queried FK
    # ADDED: onupdate="CASCADE" for strict referential integrity
    created_by = Column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True,
        index=True
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    creator = relationship("User", back_populates="projects_owned")
    projects = relationship("Project", back_populates="client")

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(
        Integer,
        ForeignKey("clients.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True
    )
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String, default="active", index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    client = relationship("Client", back_populates="projects")
    members = relationship(
        "ProjectMember",
        back_populates="project",
        cascade="all, delete-orphan"
    )
    tasks = relationship(
        "Task",
        back_populates="project",
        cascade="all, delete-orphan"
    )
    logged_hours = relationship("LoggedHour", back_populates="project")
    git_contributions = relationship("GitContribution", back_populates="project")

    @property
    def total_logged_hours(self) -> float:
        return sum(lh.hours for lh in self.logged_hours)

class ProjectMember(Base):
    __tablename__ = "project_members"

    # ADDED: Composite Unique Constraint
    # Ensures a user isn't added to a project twice
    __table_args__ = (
        UniqueConstraint('project_id', 'user_id', name='uix_project_member'),
    )

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(
        Integer,
        ForeignKey("projects.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True
    )
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True
    )
    role = Column(String, default="member")
    added_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    project = relationship("Project", back_populates="members")
    user = relationship("User", back_populates="project_memberships")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(
        Integer,
        ForeignKey("projects.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True
    )
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String, default="todo", index=True)

    # Foreign Key with SET NULL on delete
    assigned_to = Column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True,
        index=True
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
        server_default=func.now()
    )

    # Relationships
    project = relationship("Project", back_populates="tasks")
    assignee = relationship("User", back_populates="tasks_assigned")
    logged_hours = relationship("LoggedHour", back_populates="task")

class LoggedHour(Base):
    __tablename__ = "logged_hours"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True
    )
    task_id = Column(
        Integer,
        ForeignKey("tasks.id", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True,
        index=True
    )
    project_id = Column(
        Integer,
        ForeignKey("projects.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True
    )
    hours = Column(Float, nullable=False)
    note = Column(Text, nullable=True)
    logged_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="logged_hours")
    task = relationship("Task", back_populates="logged_hours")
    project = relationship("Project", back_populates="logged_hours")

class GitContribution(Base):
    __tablename__ = "git_contributions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True,
        index=True
    )
    project_id = Column(
        Integer,
        ForeignKey("projects.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True
    )

    # Unique Constraint explicitly required
    commit_hash = Column(String, nullable=False, unique=True)

    commit_message = Column(Text, nullable=True)
    branch = Column(String, nullable=True)
    committed_at = Column(DateTime(timezone=True), nullable=False)

    # Relationships
    user = relationship("User", back_populates="git_contributions")
    project = relationship("Project", back_populates="git_contributions")

class SystemLog(Base):
    __tablename__ = "system_logs"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    meta = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# --- Initialization Logic ---

def init_db():
    logger.info("Starting database initialization process.")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(
            "FATAL DB ERROR: Could not complete schema creation: %s",
            e,
            exc_info=True
        )
        raise e

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
