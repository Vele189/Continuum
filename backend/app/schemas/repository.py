from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class RepositoryBase(BaseModel):
    repository_url: str
    repository_name: str
    provider: str
    is_active: bool = True

class RepositoryCreate(RepositoryBase):
    project_id: int
    webhook_secret: Optional[str] = None

class RepositoryUpdate(BaseModel):
    is_active: Optional[bool] = None
    webhook_secret: Optional[str] = None

class RepositoryOut(RepositoryBase):
    id: int
    project_id: int
    webhook_secret: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
