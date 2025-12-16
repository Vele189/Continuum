from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String)
    status = Column(String, default="To Do")
    assigned_to = Column(Integer, ForeignKey("users.id"))
    created_at = Column(String, default=func.now())
    updated_at = Column(String, default=func.now(), onupdate=func.now())

    project = relationship("Project", back_populates="tasks")
    assignee = relationship("User", backref="tasks")
