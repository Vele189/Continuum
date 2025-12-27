"""
Service layer for task attachment business logic.
"""

from typing import List, Optional

from app.api.deps import is_admin_user
from app.dbmodels import Task, TaskAttachment, User
from app.services import task as task_service
from app.utils.file_upload import delete_file, get_file_content, save_uploaded_file
from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session


def validate_task_access(db: Session, task_id: int, user_id: int) -> Task:
    """
    Validate that a user has access to a task (must be project member or admin).

    Returns:
        The task if access is granted

    Raises:
        HTTPException if task not found or access denied
    """
    task = task_service.get(db, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    # Admins have access to all tasks
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if is_admin_user(user):
        return task

    # Regular users must be project members
    if not task_service.validate_project_membership(db, task.project_id, user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not a member of this project"
        )

    return task


def can_delete_attachment(db: Session, attachment_id: int, user_id: int) -> bool:
    """
    Check if a user can delete an attachment.

    Rules:
    - Uploader can delete their own attachments
    - Admins can delete any attachment

    Returns:
        True if user can delete, False otherwise
    """
    attachment = db.query(TaskAttachment).filter(TaskAttachment.id == attachment_id).first()
    if not attachment:
        return False

    # Uploader can delete
    if attachment.user_id == user_id:
        return True

    # Admins can delete
    user = db.query(User).filter(User.id == user_id).first()
    if user and is_admin_user(user):
        return True

    return False


async def create(
    db: Session, upload_file: UploadFile, task_id: int, user_id: int
) -> TaskAttachment:
    """
    Upload a file attachment to a task.

    Args:
        db: Database session
        upload_file: The uploaded file
        task_id: ID of the task
        user_id: ID of the user uploading

    Returns:
        Created TaskAttachment object

    Raises:
        HTTPException if validation fails
    """
    # Validate task access
    validate_task_access(db, task_id, user_id)

    # Save file and get metadata
    filename, file_path, file_size, mime_type = await save_uploaded_file(
        upload_file, task_id, user_id
    )

    # Create attachment record
    attachment = TaskAttachment(
        task_id=task_id,
        user_id=user_id,
        filename=filename,
        original_filename=upload_file.filename or "unnamed_file",
        file_path=file_path,
        file_size=file_size,
        mime_type=mime_type,
    )

    db.add(attachment)
    db.commit()
    db.refresh(attachment)

    return attachment


def get_by_id(db: Session, attachment_id: int) -> Optional[TaskAttachment]:
    """Get an attachment by ID."""
    return db.query(TaskAttachment).filter(TaskAttachment.id == attachment_id).first()


def get_by_task(db: Session, task_id: int) -> List[TaskAttachment]:
    """
    Get all attachments for a task.

    Note: This method doesn't load relationships. Use joinedload in the route
    if you need the uploader relationship.
    """
    return db.query(TaskAttachment).filter(TaskAttachment.task_id == task_id).all()


def get_file_bytes(db: Session, attachment_id: int, user_id: int) -> tuple[bytes, str, str]:
    """
    Get file content for download.

    Args:
        db: Database session
        attachment_id: ID of the attachment
        user_id: ID of the user requesting download

    Returns:
        Tuple of (file_content, filename, mime_type)

    Raises:
        HTTPException if attachment not found or access denied
    """
    attachment = get_by_id(db, attachment_id)
    if not attachment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attachment not found")

    # Validate task access
    validate_task_access(db, attachment.task_id, user_id)

    # Get file content
    file_content = get_file_content(attachment.file_path)

    return file_content, attachment.original_filename, attachment.mime_type


def delete(db: Session, attachment_id: int, user_id: int) -> bool:
    """
    Delete an attachment.

    Args:
        db: Database session
        attachment_id: ID of the attachment to delete
        user_id: ID of the user requesting deletion

    Returns:
        True if deletion was successful

    Raises:
        HTTPException if attachment not found, access denied, or deletion fails
    """
    attachment = get_by_id(db, attachment_id)
    if not attachment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attachment not found")

    # Check permissions
    if not can_delete_attachment(db, attachment_id, user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this attachment",
        )

    # Delete file from storage
    file_deleted = delete_file(attachment.file_path)
    if not file_deleted:
        # Log warning but continue with DB deletion
        pass

    # Delete from database
    db.delete(attachment)
    db.commit()

    return True
