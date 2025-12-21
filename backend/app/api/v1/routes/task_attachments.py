"""
API routes for task attachments.
"""
from fastapi import APIRouter, Depends, status, UploadFile, File
from fastapi.responses import Response
from sqlalchemy.orm import Session, joinedload

from app.api import deps
from app.database import User, TaskAttachment
from app.schemas.task_attachment import TaskAttachment as TaskAttachmentSchema, TaskAttachmentList
from app.services import task_attachment as attachment_service

router = APIRouter()


@router.post(
    "/tasks/{task_id}/attachments",
    response_model=TaskAttachmentSchema,
    status_code=status.HTTP_201_CREATED
)
async def upload_attachment(
    task_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Upload a file attachment to a task.

    Requires the user to be a member of the project (or admin).
    """
    attachment = await attachment_service.create(
        db=db,
        upload_file=file,
        task_id=task_id,
        user_id=current_user.id
    )

    # Reload with relationships for response
    attachment = db.query(TaskAttachment).options(
        joinedload(TaskAttachment.uploader)
    ).filter(TaskAttachment.id == attachment.id).first()

    return attachment


@router.get(
    "/tasks/{task_id}/attachments",
    response_model=TaskAttachmentList
)
def list_attachments(
    task_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    List all attachments for a task.

    Requires the user to be a member of the project (or admin).
    """
    # Validate task access
    attachment_service.validate_task_access(db, task_id, current_user.id)

    # Get attachments with uploader relationship loaded
    attachments = db.query(TaskAttachment).options(
        joinedload(TaskAttachment.uploader)
    ).filter(TaskAttachment.task_id == task_id).all()

    return TaskAttachmentList(
        attachments=attachments,
        total=len(attachments)
    )


@router.get("/attachments/{attachment_id}/download")
def download_attachment(
    attachment_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Download an attachment.

    Requires the user to be a member of the project (or admin).
    """
    file_content, filename, mime_type = attachment_service.get_file_bytes(
        db=db,
        attachment_id=attachment_id,
        user_id=current_user.id
    )

    return Response(
        content=file_content,
        media_type=mime_type,
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        }
    )


@router.delete(
    "/attachments/{attachment_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_attachment(
    attachment_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Delete an attachment.

    Only the uploader or an admin can delete an attachment.
    """
    attachment_service.delete(
        db=db,
        attachment_id=attachment_id,
        user_id=current_user.id
    )
