from datetime import datetime
from typing import List, Dict
from pydantic import BaseModel, ConfigDict


class SummaryDateRange(BaseModel):
    earliest: datetime
    latest: datetime


class SummaryMetadata(BaseModel):
    total_tasks: int
    total_commits: int
    total_logged_hours: int
    date_range: SummaryDateRange
    task_count_by_status: Dict[str, int]


class ProjectSummary(BaseModel):
    project_id: int
    project_name: str
    task_descriptions: List[str]
    commit_messages: List[str]
    logged_hour_notes: List[str]
    aggregated_text: str
    metadata: SummaryMetadata
    generated_at: datetime

    model_config = ConfigDict(from_attributes=True)
