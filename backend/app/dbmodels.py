# app/models.py
# pylint: disable=not-callable
import enum
import logging

from app.db.base import Base
from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

# --- Logger Setup ---
try:
    from utils.logger import get_logger
except ImportError:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s | [%(name)s] %(message)s")

    def get_logger(name: str):
        return logging.getLogger(name)


logger = get_logger(__name__)


class UserRole(enum.Enum):
    BACKEND = "backend"
    FRONTEND = "frontend"
    DESIGNER = "designer"
    CLIENT = "client"
    PROJECTMANAGER = "project_manager"
    ADMIN = "admin"


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
    hourly_rate = Column(Numeric(10, 2), default=0.0)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.FRONTEND)
    is_verified = Column(Boolean, default=False)
    verification_token = Column(String(255))
    refresh_token = Column(String(255), nullable=True)
    password_reset_token = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    skills = Column(JSON, nullable=True)  # User skills stored as JSON array

    # Relationships
    projects_owned = relationship("Client", back_populates="creator")
    tasks_assigned = relationship("Task", back_populates="assignee")
    logged_hours = relationship("LoggedHour", back_populates="user")
    git_contributions = relationship("GitContribution", back_populates="user")
    project_memberships = relationship("ProjectMember", back_populates="user")
    task_attachments = relationship("TaskAttachment", back_populates="uploader")
    task_comments = relationship("TaskComment", back_populates="author")


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
        index=True,
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
        index=True,
    )
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String, default="active", index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    client = relationship("Client", back_populates="projects")
    members = relationship("ProjectMember", back_populates="project", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")
    logged_hours = relationship("LoggedHour", back_populates="project")
    git_contributions = relationship("GitContribution", back_populates="project")
    invoices = relationship("Invoice", back_populates="project")
    milestones = relationship("Milestone", back_populates="project")


class ProjectMember(Base):
    __tablename__ = "project_members"

    # ADDED: Composite Unique Constraint
    # Ensures a user isn't added to a project twice
    __table_args__ = (UniqueConstraint("project_id", "user_id", name="uix_project_member"),)

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(
        Integer,
        ForeignKey("projects.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
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
        index=True,
    )
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String, default="todo", index=True)
    milestone_id = Column(
        Integer,
        ForeignKey("milestones.id", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True,
        index=True,
    )

    # Foreign Key with SET NULL on delete
    assigned_to = Column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True,
        index=True,
    )
    due_date = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # Relationships
    project = relationship("Project", back_populates="tasks")
    assignee = relationship("User", back_populates="tasks_assigned")
    logged_hours = relationship("LoggedHour", back_populates="task")
    milestone = relationship("Milestone", back_populates="tasks")
    attachments = relationship(
        "TaskAttachment", back_populates="task", cascade="all, delete-orphan"
    )
    comments = relationship("TaskComment", back_populates="task", cascade="all, delete-orphan")


class LoggedHour(Base):
    __tablename__ = "logged_hours"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    task_id = Column(
        Integer,
        ForeignKey("tasks.id", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True,
        index=True,
    )
    project_id = Column(
        Integer,
        ForeignKey("projects.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
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

    # Composite Unique Constraint: same commit hash cannot be linked twice to the same project
    __table_args__ = (UniqueConstraint("project_id", "commit_hash", name="uix_project_commit"),)

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    project_id = Column(
        Integer,
        ForeignKey("projects.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    task_id = Column(
        Integer,
        ForeignKey("tasks.id", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True,
        index=True,
    )

    commit_hash = Column(String, nullable=False, index=True)
    branch = Column(String, nullable=True)
    commit_message = Column(Text, nullable=True)
    provider = Column(String, nullable=False)  # e.g., "github", "gitlab"
    commit_url = Column(String, nullable=True)

    # Legacy column - kept for database compatibility, use created_at instead
    committed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="git_contributions")
    project = relationship("Project", back_populates="git_contributions")
    task = relationship("Task", backref="git_contributions")


class Milestone(Base):
    __tablename__ = "milestones"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(
        Integer,
        ForeignKey("projects.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    name = Column(String, nullable=False)
    due_date = Column(DateTime(timezone=True), nullable=True)
    status = Column(String, default="not_started")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # Relationships
    project = relationship("Project", back_populates="milestones")
    tasks = relationship("Task", back_populates="milestone")


class SystemLog(Base):
    __tablename__ = "system_logs"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    meta = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class InvoiceStatus(enum.Enum):
    """Invoice lifecycle status"""

    DRAFT = "draft"
    SENT = "sent"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(
        Integer,
        ForeignKey("projects.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    invoice_number = Column(String, unique=True, nullable=False, index=True)
    status = Column(Enum(InvoiceStatus), default=InvoiceStatus.DRAFT, nullable=False, index=True)

    # Billing period
    billing_period_start = Column(DateTime(timezone=True), nullable=False)
    billing_period_end = Column(DateTime(timezone=True), nullable=False)

    # Financial totals (stored as immutable snapshots)
    subtotal = Column(Numeric(10, 2), nullable=False)
    tax_rate = Column(Numeric(5, 4), default=0.0, nullable=False)  # e.g., 0.1000 for 10%
    tax_amount = Column(Numeric(10, 2), default=0.0, nullable=False)
    total = Column(Numeric(10, 2), nullable=False)

    # PDF storage
    pdf_path = Column(String, nullable=True)

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    created_by = Column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True,
        index=True,
    )

    # Relationships
    project = relationship("Project", back_populates="invoices")
    items = relationship("InvoiceItem", back_populates="invoice", cascade="all, delete-orphan")
    creator = relationship("User", foreign_keys=[created_by])


class InvoiceItem(Base):
    __tablename__ = "invoice_items"

    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(
        Integer,
        ForeignKey("invoices.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )

    # Snapshot of logged hour data (immutable)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    task_id = Column(
        Integer,
        ForeignKey("tasks.id", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True,
        index=True,
    )
    logged_hour_id = Column(
        Integer,
        ForeignKey("logged_hours.id", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True,
        index=True,
    )

    # Immutable billing data
    description = Column(Text, nullable=True)
    hours = Column(Numeric(10, 2), nullable=False)
    hourly_rate = Column(Numeric(10, 2), nullable=False)  # Snapshot at generation time
    line_total = Column(Numeric(10, 2), nullable=False)  # hours * hourly_rate

    # Date of work (from logged hour)
    work_date = Column(DateTime(timezone=True), nullable=False)

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    invoice = relationship("Invoice", back_populates="items")
    user = relationship("User", foreign_keys=[user_id])
    task = relationship("Task", foreign_keys=[task_id])
    logged_hour = relationship("LoggedHour", foreign_keys=[logged_hour_id])


class TaskAttachment(Base):
    __tablename__ = "task_attachments"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(
        Integer,
        ForeignKey("tasks.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    filename = Column(String, nullable=False)  # Internal/storage-safe name
    original_filename = Column(String, nullable=False)  # User-uploaded name
    file_path = Column(String, nullable=False)  # Storage location
    file_size = Column(Integer, nullable=False)  # Size in bytes
    mime_type = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # Relationships
    task = relationship("Task", back_populates="attachments")
    uploader = relationship("User", back_populates="task_attachments")


class TaskComment(Base):
    __tablename__ = "task_comments"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(
        Integer,
        ForeignKey("tasks.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True,
        index=True,
    )
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # Relationships
    task = relationship("Task", back_populates="comments")
    author = relationship("User", back_populates="task_comments")


# --- Initialization Logic ---
# removed for testing
