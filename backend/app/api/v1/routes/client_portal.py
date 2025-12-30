from app.utils.logger import get_logger
from backend.app.api import deps
from backend.app.dbmodels import Client
from backend.app.schemas.project import ProjectProgress
from backend.app.schemas.user import User
from backend.app.services.project import ProjectService
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from sqlalchemy.orm import Session

logger = get_logger(__name__)
router = APIRouter()


@router.get("/projects/{id}/progress",response_model=ProjectProgress)
def get_project_progress_route(
    project_id: int,
    db: Session = Depends(deps.get_db),
    client: Client = Depends(deps.get_current_user),
):
    return ProjectService.get_project_progress(
        db=db,
        project_id=project_id,
        client=client,
    )