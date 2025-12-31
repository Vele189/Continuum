"""
Schemas for task timeline/activity feed.

This module defines the data structures for a unified, chronological
activity timeline that aggregates all task-related actions.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel


class ActivityType(str, Enum):
    """Enumeration of all possible activity types in the timeline."""

    TASK_CREATED = "task_created"
    STATUS_CHANGED = "status_changed"
    ASSIGNMENT_CHANGED = "assignment_changed"
    COMMENT_ADDED = "comment_added"
    ATTACHMENT_UPLOADED = "attachment_uploaded"
    HOURS_LOGGED = "hours_logged"
    COMMIT_LINKED = "commit_linked"


class ActivityUser(BaseModel):
    """User information for an activity."""

    id: int
    name: Optional[str] = None
    email: Optional[str] = None
    display_name: Optional[str] = None


class TimelineActivity(BaseModel):
    """
    A single activity entry in the timeline.

    All activities follow this unified structure regardless of source.
    """

    # Unique identifier for this activity
    # Format: "{activity_type}_{source_id}" (e.g., "attachment_uploaded_123")
    id: str

    # Type of activity
    activity_type: ActivityType

    # User who performed the activity (if applicable)
    user: Optional[ActivityUser] = None

    # Timestamp when the activity occurred
    timestamp: datetime

    # Type-specific data payload
    # Structure varies by activity_type:
    # - task_created: {title, description, status, assigned_to}
    # - status_changed: {old_status, new_status}
    # - assignment_changed: {old_assignee_id, old_assignee_name, new_assignee_id, new_assignee_name}
    # - comment_added: {comment_id, content}
    # - attachment_uploaded: {attachment_id, filename, file_size, mime_type}
    # - hours_logged: {logged_hour_id, hours, description, date}
    # - commit_linked: {commit_id, commit_hash, commit_message, branch, provider}
    data: Dict[str, Any]


class TaskTimelineResponse(BaseModel):
    """
    Response schema for the task timeline endpoint.

    Returns a paginated list of activities in chronological order.
    """

    activities: list[TimelineActivity]
    total: int
    skip: int
    limit: int
