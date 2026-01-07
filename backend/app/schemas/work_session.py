from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, computed_field
from app.dbmodels import WorkSessionStatus

class WorkSessionBase(BaseModel):
    project_id: int
    task_id: Optional[int] = None
    note: Optional[str] = None

class WorkSessionCreate(WorkSessionBase):
    pass

class WorkSessionUpdate(BaseModel):
    note: Optional[str] = None

class WorkSessionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    project_id: int
    task_id: Optional[int] = None
    started_at: datetime
    ended_at: Optional[datetime] = None
    last_resumed_at: Optional[datetime] = None
    duration_seconds: int
    status: WorkSessionStatus
    note: Optional[str] = None

    @computed_field
    @property
    def current_duration_seconds(self) -> int:
        if self.status == WorkSessionStatus.ACTIVE and self.last_resumed_at:
            # Calculate elapsed time since last resume
            # Using datetime.now() to match naive datetime if that's what's in DB
            # If DB is timezone-aware, this might need adjustment
            now = datetime.now()
            # If last_resumed_at has timezone and now doesn't, this will fail
            # We assume consistency here.
            elapsed = int((now - self.last_resumed_at.replace(tzinfo=None)).total_seconds())
            return self.duration_seconds + elapsed
        return self.duration_seconds

class WorkSessionAction(BaseModel):
    pass
