from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_admin, get_current_user, is_admin_user
from app.dbmodels import User
from app.schemas.repository import RepositoryCreate, RepositoryOut
from app.services import repository as repository_service
from app.services.project import ProjectService

router = APIRouter()

@router.post("/projects/{project_id}/repositories", response_model=RepositoryOut, status_code=status.HTTP_201_CREATED)
def link_repository(
    project_id: int,
    repo_in: RepositoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin),
):
    """
    Link a repository to a project.
    
    Requires admin privileges.
    """
    # Ensure project_id in path matches project_id in body
    if repo_in.project_id != project_id:
        repo_in.project_id = project_id
        
    return repository_service.link_repository(db, repo_in)

@router.get("/projects/{project_id}/repositories", response_model=List[RepositoryOut])
def list_repositories(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    List repositories linked to a project.
    
    - Admins can view any project's repositories
    - Members can view repositories of projects they belong to
    """
    is_admin = is_admin_user(current_user)
    # Verify access to project first
    ProjectService.get_project_with_check(db, project_id, current_user.id, is_admin=is_admin)
    
    return repository_service.get_repositories_by_project(db, project_id)

@router.delete("/repositories/{repository_id}", status_code=status.HTTP_204_NO_CONTENT)
def unlink_repository(
    repository_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin),
):
    """
    Unlink a repository.
    
    Requires admin privileges.
    """
    repository_service.unlink_repository(db, repository_id)
