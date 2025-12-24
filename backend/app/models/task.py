from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String)
    status = Column(String, default="todo")
    milestone_id = Column(Integer, ForeignKey("milestones.id", ondelete="SET NULL", onupdate="CASCADE"), nullable=True)
    assigned_to = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    project = relationship("Project", back_populates="tasks")
    milestone = relationship("Milestone", back_populates="tasks")
    assignee = relationship("User", backref="tasks")
