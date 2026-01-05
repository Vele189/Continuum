from app.api import deps
from app.dbmodels import Client
from app.schemas.project import ClientPortalProject
from app.services.project import ProjectService
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/projects/{id}", response_model=ClientPortalProject)
def get_client_portal_project(
    id: int, db: Session = Depends(deps.get_db), client: Client = Depends(deps.get_current_client)
):
    """
    Expose a sanitized, read-only project view for clients via the Client Portal.
    """
    return ProjectService.get_client_portal_project(db, project_id=id, client=client)
