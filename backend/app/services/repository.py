from typing import List

from app.dbmodels import Project, Repository
from app.schemas.repository import RepositoryCreate, RepositoryUpdate
from fastapi import HTTPException, status
from sqlalchemy.orm import Session


def normalize_repository_url(url: str) -> str:
    """
    Normalize repository URL for comparison.
    - Remove trailing .git
    - Remove trailing slash
    - Lowercase
    """
    if not url:
        return ""
    url = url.strip().lower()
    if url.endswith(".git"):
        url = url[:-4]
    if url.endswith("/"):
        url = url[:-1]
    return url


def link_repository(db: Session, data: RepositoryCreate) -> Repository:
    """Create and persist a repository → project mapping"""
    # Normalize URL before comparison and storage
    data.repository_url = normalize_repository_url(data.repository_url)

    # Check if project exists
    project = db.query(Project).filter(Project.id == data.project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {data.project_id} not found",
        )

    # Prevent duplicate repository URLs
    existing = db.query(Repository).filter(Repository.repository_url == data.repository_url).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Repository with URL {data.repository_url} is already linked to project {existing.project_id}",
        )

    db_repo = Repository(**data.model_dump())
    db.add(db_repo)
    db.commit()
    db.refresh(db_repo)
    return db_repo


def get_repositories_by_project(db: Session, project_id: int) -> List[Repository]:
    """Return all active repositories for a project"""
    return (
        db.query(Repository)
        .filter(Repository.project_id == project_id, Repository.is_active == True)  # noqa: E712
        .all()
    )


def unlink_repository(db: Session, repo_id: int) -> None:
    """Delete or deactivate a repository mapping (hard delete)"""
    db_repo = db.query(Repository).filter(Repository.id == repo_id).first()
    if not db_repo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Repository with id {repo_id} not found",
        )

    db.delete(db_repo)
    db.commit()


def update_repository(db: Session, repo_id: int, data: RepositoryUpdate) -> Repository:
    """Update repository settings"""
    db_repo = db.query(Repository).filter(Repository.id == repo_id).first()
    if not db_repo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Repository with id {repo_id} not found",
        )

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_repo, key, value)

    db.commit()
    db.refresh(db_repo)
    return db_repo
