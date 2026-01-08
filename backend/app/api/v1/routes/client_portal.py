from app.api import deps
from app.dbmodels import Client
from app.schemas.project import ProjectProgress
from app.services.project import ProjectService
from app.utils.logger import get_logger
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

logger = get_logger(__name__)
router = APIRouter()


@router.get("/projects/{project_id}/progress", response_model=ProjectProgress)
def get_project_progress_route(
    project_id: int,
    activity_limit: int = Query(
        10, ge=1, le=50, description="Maximum number of recent activity items to return"
    ),
    db: Session = Depends(deps.get_db),
    client: Client = Depends(deps.get_current_client),
):
    return ProjectService.get_project_progress(
        db=db,
        project_id=project_id,
        client=client,
        activity_limit=activity_limit,
    )
