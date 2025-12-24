from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.database import TaskComment, Task, User, UserRole
from app.schemas.task_comment import TaskCommentCreate, TaskCommentUpdate
from app.services.task import validate_project_membership


def create_comment(
    db: Session,
    task_id: int,
    user_id: int,
    content: str
) -> TaskComment:
    """
    Create a new comment on a task.
    
    Args:
        db: Database session
        task_id: ID of the task to comment on
        user_id: ID of the user creating the comment
        content: Comment content
        
    Returns:
        Created TaskComment
        
    Raises:
        HTTPException: If task not found or user not a project member
    """
    # Validate task exists
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Validate user is a project member (will be checked at route level too)
    # This is a safety check
    if not validate_project_membership(db, task.project_id, user_id):
        raise HTTPException(
            status_code=403,
            detail="User is not a member of this project"
        )
    
    # Create comment
    comment = TaskComment(
        task_id=task_id,
        user_id=user_id,
        content=content
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


def get_comments(db: Session, task_id: int) -> List[TaskComment]:
    """
    Get all comments for a task in chronological order (oldest first).
    
    Args:
        db: Database session
        task_id: ID of the task
        
    Returns:
        List of TaskComment objects ordered by created_at
    """
    return db.query(TaskComment).filter(
        TaskComment.task_id == task_id
    ).order_by(TaskComment.created_at.asc()).all()


def get_comment(db: Session, comment_id: int) -> Optional[TaskComment]:
    """
    Get a single comment by ID.
    
    Args:
        db: Database session
        comment_id: ID of the comment
        
    Returns:
        TaskComment or None if not found
    """
    return db.query(TaskComment).filter(TaskComment.id == comment_id).first()


def update_comment(
    db: Session,
    comment_id: int,
    user_id: int,
    content: str,
    is_admin: bool = False
) -> TaskComment:
    """
    Update a comment's content.
    
    Only the comment author can update their comment.
    
    Args:
        db: Database session
        comment_id: ID of the comment to update
        user_id: ID of the user attempting the update
        content: New content
        is_admin: Whether the user is an admin (bypasses ownership check)
        
    Returns:
        Updated TaskComment
        
    Raises:
        HTTPException: If comment not found or user not authorized
    """
    comment = get_comment(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    # Only comment author can update (admins don't bypass this - they can only delete)
    if comment.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="You can only update your own comments"
        )
    
    comment.content = content
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


def delete_comment(
    db: Session,
    comment_id: int,
    user_id: int,
    user_role: UserRole
) -> TaskComment:
    """
    Delete a comment.
    
    Comment author can delete their own comment.
    ADMIN role can delete any comment (bypasses ownership).
    PROJECTMANAGER role requires ownership.
    
    Args:
        db: Database session
        comment_id: ID of the comment to delete
        user_id: ID of the user attempting the deletion
        user_role: Role of the user
        
    Returns:
        Deleted TaskComment
        
    Raises:
        HTTPException: If comment not found or user not authorized
    """
    comment = get_comment(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    # ADMIN can delete any comment
    # Others can only delete their own
    is_owner = comment.user_id == user_id
    is_system_admin = user_role == UserRole.ADMIN
    
    if not is_owner and not is_system_admin:
        raise HTTPException(
            status_code=403,
            detail="You can only delete your own comments"
        )
    
    db.delete(comment)
    db.commit()
    return comment
