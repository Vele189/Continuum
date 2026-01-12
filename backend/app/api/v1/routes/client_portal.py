from app.api import deps
from app.dbmodels import Client
from app.schemas.project import ClientPortalProject, ProjectProgress
from app.services.project import ProjectService
from app.utils.logger import get_logger
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

logger = get_logger(__name__)
router = APIRouter()


@router.get("/projects/{id}", response_model=ClientPortalProject)
def get_client_portal_project(
    id: int,
    db: Session = Depends(deps.get_db),
    client: Client = Depends(deps.get_current_client_by_token),
):
    """
    Expose a sanitized, read-only project view for clients via the Client Portal.
    """
    return ProjectService.get_client_portal_project(db, project_id=id, client=client)


@router.get("/projects/{project_id}/progress", response_model=ProjectProgress)
def get_project_progress_route(
    project_id: int,
    activity_limit: int = Query(
        10, ge=1, le=50, description="Maximum number of recent activity items to return"
    ),
    db: Session = Depends(deps.get_db),
    client: Client = Depends(deps.get_current_client),
):
    """
    Get project progress for a client (user-based authentication).
    """
    return ProjectService.get_project_progress(
        db=db,
        project_id=project_id,
        client=client,
        activity_limit=activity_limit,
    )
