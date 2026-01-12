# pylint: disable=unused-argument
from typing import List

from app.api import deps
from app.dbmodels import Task, User, UserRole
from app.schemas.task_comment import TaskComment, TaskCommentCreate, TaskCommentUpdate
from app.services import task_comment as comment_service
from app.services.task import validate_project_membership
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter()


def _enrich_comment_with_author(comment) -> dict:
    """Helper to add author info to comment response."""
    comment_dict = {
        "id": comment.id,
        "task_id": comment.task_id,
        "user_id": comment.user_id,
        "content": comment.content,
        "created_at": comment.created_at,
        "updated_at": comment.updated_at,
        "author": None,
    }

    if comment.author:
        comment_dict["author"] = {
            "id": comment.author.id,
            "display_name": comment.author.display_name,
            "username": comment.author.username,
        }

    return comment_dict


@router.post(
    "/tasks/{task_id}/comments", response_model=TaskComment, status_code=status.HTTP_201_CREATED
)
def create_comment(
    task_id: int,
    comment_in: TaskCommentCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Create a new comment on a task.

    Requires:
    - User must be authenticated
    - ADMIN: No membership required
    - PROJECTMANAGER: Must be a project member
    - Other roles: Must be a project member
    """
    # Get task to validate it exists and get project_id
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # ADMIN bypasses membership check, others need membership
    if current_user.role != UserRole.ADMIN:
        if not validate_project_membership(db, task.project_id, current_user.id):
            raise HTTPException(status_code=403, detail="Not a member of this project")

    comment = comment_service.create_comment(
        db=db, task_id=task_id, user_id=current_user.id, content=comment_in.content
    )

    return _enrich_comment_with_author(comment)


@router.get("/tasks/{task_id}/comments", response_model=List[TaskComment])
def list_comments(
    task_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Get all comments for a task in chronological order.

    Requires:
    - User must be authenticated
    - ADMIN: No membership required
    - PROJECTMANAGER: Must be a project member
    - Other roles: Must be a project member
    """
    # Get task to validate it exists and get project_id
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # ADMIN bypasses membership check, others need membership
    if current_user.role != UserRole.ADMIN:
        if not validate_project_membership(db, task.project_id, current_user.id):
            raise HTTPException(status_code=403, detail="Not a member of this project")

    comments = comment_service.get_comments(db=db, task_id=task_id)
    return [_enrich_comment_with_author(comment) for comment in comments]


@router.put("/comments/{comment_id}", response_model=TaskComment)
def update_comment(
    comment_id: int,
    comment_in: TaskCommentUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Update a comment.

    Only the comment author can update their comment.
    Admins cannot update others' comments (only delete).
    """
    # Get comment first to check task membership
    comment = comment_service.get_comment(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    # Get task to validate membership
    task = db.query(Task).filter(Task.id == comment.task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # ADMIN bypasses membership check for viewing, but still needs ownership to update
    if current_user.role != UserRole.ADMIN:
        if not validate_project_membership(db, task.project_id, current_user.id):
            raise HTTPException(status_code=403, detail="Not a member of this project")

    updated_comment = comment_service.update_comment(
        db=db,
        comment_id=comment_id,
        user_id=current_user.id,
        content=comment_in.content,
    )

    return _enrich_comment_with_author(updated_comment)


@router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    comment_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Delete a comment.

    - Comment author can delete their own comment
    - ADMIN can delete any comment (no membership required)
    - PROJECTMANAGER can only delete their own comments (requires membership)
    """
    # Get comment first to check task membership
    comment = comment_service.get_comment(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    # Get task to validate membership
    task = db.query(Task).filter(Task.id == comment.task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # ADMIN bypasses membership check, others need membership
    if current_user.role != UserRole.ADMIN:
        if not validate_project_membership(db, task.project_id, current_user.id):
            raise HTTPException(status_code=403, detail="Not a member of this project")

    comment_service.delete_comment(
        db=db, comment_id=comment_id, user_id=current_user.id, user_role=current_user.role
    )
