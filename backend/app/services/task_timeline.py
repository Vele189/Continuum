"""
Service for aggregating task timeline activities.

This service collects activities from multiple sources and normalizes them
into a unified chronological timeline.
"""
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException

from app.dbmodels import (
    Task,
    TaskAttachment,
    LoggedHour,
    GitContribution,
    User
)
from app.schemas.task_timeline import (
    TimelineActivity,
    ActivityType,
    ActivityUser
)
from app.services.task import validate_project_membership


def _build_activity_user(user: Optional[User]) -> Optional[ActivityUser]:
    """Build ActivityUser from User model."""
    if not user:
        return None

    display_name = user.display_name or f"{user.first_name} {user.last_name}".strip()
    return ActivityUser(
        id=user.id,
        name=display_name,
        email=user.email,
        display_name=user.display_name
    )


def _get_task_created_activity(task: Task) -> TimelineActivity:
    """
    Create activity for task creation.

    Note: Task model doesn't have a created_by field, so we can't
    determine who created the task. User will be None.
    """
    return TimelineActivity(
        id=f"task_created_{task.id}",
        activity_type=ActivityType.TASK_CREATED,
        user=None,  # Can't determine creator without created_by field
        timestamp=task.created_at,
        data={
            "task_id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "assigned_to": task.assigned_to,
        }
    )


def _get_status_changed_activity(task: Task) -> Optional[TimelineActivity]:
    """
    Create activity for status change.

    Note: This only captures the current status. For full history,
    a task_activities table would be needed to track all status transitions.
    """
    # Since we don't have historical tracking, we'll use updated_at
    # This will only show the last status change, not all changes
    # Compare timestamps to avoid timezone issues
    if task.created_at and task.updated_at:
        time_diff = (task.updated_at - task.created_at).total_seconds()
        if abs(time_diff) < 1:  # Less than 1 second difference
            return None  # No status change yet

    # We can't determine old_status without historical tracking
    # For now, we'll just show the current status
    timestamp = task.updated_at if task.updated_at else task.created_at
    return TimelineActivity(
        id=f"status_changed_{task.id}_{timestamp.timestamp() if timestamp else 0}",
        activity_type=ActivityType.STATUS_CHANGED,
        user=None,  # Can't determine who changed it without history
        timestamp=timestamp,
        data={
            "task_id": task.id,
            "new_status": task.status,
            "old_status": None,  # Unknown without historical tracking
        }
    )


def _get_assignment_changed_activity(task: Task) -> Optional[TimelineActivity]:
    """
    Create activity for assignment change.

    Note: This only captures the current assignment. For full history,
    a task_activities table would be needed to track all assignment changes.
    """
    # Compare timestamps to avoid timezone issues
    if task.created_at and task.updated_at:
        time_diff = (task.updated_at - task.created_at).total_seconds()
        if abs(time_diff) < 1:  # Less than 1 second difference
            return None  # No assignment change yet

    assignee = _build_activity_user(task.assignee) if task.assignee else None
    timestamp = task.updated_at if task.updated_at else task.created_at

    return TimelineActivity(
        id=f"assignment_changed_{task.id}_{timestamp.timestamp() if timestamp else 0}",
        activity_type=ActivityType.ASSIGNMENT_CHANGED,
        user=None,  # Can't determine who changed it without history
        timestamp=timestamp,
        data={
            "task_id": task.id,
            "new_assignee_id": task.assigned_to,
            "new_assignee_name": assignee.name if assignee else None,
            "old_assignee_id": None,  # Unknown without historical tracking
            "old_assignee_name": None,
        }
    )


def _get_attachment_activities(
    db: Session,
    task_id: int
) -> List[TimelineActivity]:
    """Get all attachment upload activities for a task."""
    attachments = db.query(TaskAttachment).options(
        joinedload(TaskAttachment.uploader)
    ).filter(TaskAttachment.task_id == task_id).all()

    activities = []
    for attachment in attachments:
        uploader = _build_activity_user(attachment.uploader)
        activities.append(TimelineActivity(
            id=f"attachment_uploaded_{attachment.id}",
            activity_type=ActivityType.ATTACHMENT_UPLOADED,
            user=uploader,
            timestamp=attachment.created_at,
            data={
                "attachment_id": attachment.id,
                "filename": attachment.original_filename,
                "file_size": attachment.file_size,
                "mime_type": attachment.mime_type,
            }
        ))

    return activities


def _get_logged_hour_activities(
    db: Session,
    task_id: int
) -> List[TimelineActivity]:
    """Get all logged hour activities for a task."""
    logged_hours = db.query(LoggedHour).options(
        joinedload(LoggedHour.user)
    ).filter(LoggedHour.task_id == task_id).all()

    activities = []
    for logged_hour in logged_hours:
        user = _build_activity_user(logged_hour.user)
        # Use the logged_at field for when the work was done
        timestamp = logged_hour.logged_at if logged_hour.logged_at else None

        activities.append(TimelineActivity(
            id=f"hours_logged_{logged_hour.id}",
            activity_type=ActivityType.HOURS_LOGGED,
            user=user,
            timestamp=timestamp,
            data={
                "logged_hour_id": logged_hour.id,
                "hours": float(logged_hour.hours),
                "description": logged_hour.note,
                "date": logged_hour.logged_at.isoformat() if logged_hour.logged_at else None,
            }
        ))

    return activities


def _get_commit_activities(
    db: Session,
    task_id: int
) -> List[TimelineActivity]:
    """Get all git commit activities linked to a task."""
    commits = db.query(GitContribution).options(
        joinedload(GitContribution.user)
    ).filter(GitContribution.task_id == task_id).all()

    activities = []
    for commit in commits:
        user = _build_activity_user(commit.user)
        # Use committed_at if available, otherwise created_at
        timestamp = commit.committed_at if commit.committed_at else commit.created_at

        activities.append(TimelineActivity(
            id=f"commit_linked_{commit.id}",
            activity_type=ActivityType.COMMIT_LINKED,
            user=user,
            timestamp=timestamp,
            data={
                "commit_id": commit.id,
                "commit_hash": commit.commit_hash,
                "commit_message": commit.commit_message,
                "branch": commit.branch,
                "provider": commit.provider,
                "commit_url": commit.commit_url,
            }
        ))

    return activities


def get_task_timeline(
    db: Session,
    task_id: int,
    user_id: int,
    is_admin: bool = False,
    skip: int = 0,
    limit: int = 100
) -> tuple[List[TimelineActivity], int]:
    """
    Get the complete timeline for a task.

    Aggregates activities from all sources:
    - Task creation
    - Status changes
    - Assignment changes
    - Attachments
    - Logged hours
    - Linked commits

    Args:
        db: Database session
        task_id: ID of the task
        user_id: ID of the user requesting the timeline (for access control)
        is_admin: Whether the user is an admin (admins bypass access checks)
        skip: Number of activities to skip (pagination)
        limit: Maximum number of activities to return

    Returns:
        Tuple of (activities list, total count)

    Raises:
        HTTPException if task not found or user doesn't have access
    """
    # Verify task exists
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Verify user has access to the task's project (admins bypass)
    if not is_admin:
        if not validate_project_membership(db, task.project_id, user_id):
            raise HTTPException(
                status_code=403,
                detail="Not a member of this project"
            )

    # Collect all activities
    activities: List[TimelineActivity] = []

    # Task creation
    activities.append(_get_task_created_activity(task))

    # Status change (if task was updated)
    status_activity = _get_status_changed_activity(task)
    if status_activity:
        activities.append(status_activity)

    # Assignment change (if task was updated)
    assignment_activity = _get_assignment_changed_activity(task)
    if assignment_activity:
        activities.append(assignment_activity)

    # Attachments
    activities.extend(_get_attachment_activities(db, task_id))

    # Logged hours
    activities.extend(_get_logged_hour_activities(db, task_id))

    # Linked commits
    activities.extend(_get_commit_activities(db, task_id))

    # Sort by timestamp in chronological order (oldest first, then by ID for stability)
    activities.sort(key=lambda a: (a.timestamp, a.id))

    total = len(activities)

    # Apply pagination
    paginated_activities = activities[skip:skip + limit]

    return paginated_activities, total
