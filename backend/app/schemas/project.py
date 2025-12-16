from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: str = "Active"

class Project(ProjectBase):
    id: int
    client_id: Optional[int] = None
    created_at: Optional[str] = None

    class Config:
        from_attributes = True
