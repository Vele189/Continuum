# pylint: disable=unused-argument
from typing import List, Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user, is_admin_user
from app.dbmodels import User
from app.schemas.git_contribution import (
    GitContribution,
    GitContributionCreate,
    GitContributionUpdate
)
from app.services.git_contribution import GitContributionService

router = APIRouter()


@router.post("/", response_model=GitContribution, status_code=status.HTTP_201_CREATED)
def create_contribution(
    contribution_in: GitContributionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new git contribution.

    - Authentication required
    - User must be a member of the project
    - Same commit hash cannot be linked twice to the same project
    - If task_id is provided, task must belong to the project
    """
    is_admin = is_admin_user(current_user)

    return GitContributionService.create_contribution(
        db, contribution_in, current_user.id, is_admin
    )


@router.get("/", response_model=List[GitContribution])
def list_contributions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    user_id: Optional[int] = Query(None, description="Filter by user ID"),
    project_id: Optional[int] = Query(None, description="Filter by project ID"),
    provider: Optional[str] = Query(None, description="Filter by provider (e.g., github, gitlab)"),
):
    """
    List git contributions with optional filters.

    - Authentication required
    - Admins can view all contributions
    - Regular users can only view contributions from projects they are members of
    - Filters are combinable: user_id, project_id, provider
    """
    is_admin = is_admin_user(current_user)

    return GitContributionService.list_contributions(
        db,
        current_user.id,
        is_admin=is_admin,
        user_id=user_id,
        project_id=project_id,
        provider=provider
    )


@router.get("/{contribution_id}", response_model=GitContribution)
def get_contribution(
    contribution_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get a git contribution by ID.

    - Authentication required
    - User must be a member of the project (or admin)
    """
    is_admin = is_admin_user(current_user)

    return GitContributionService.get_contribution(
        db, contribution_id, current_user.id, is_admin
    )


@router.put("/{contribution_id}", response_model=GitContribution)
def update_contribution(
    contribution_id: int,
    contribution_in: GitContributionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update a git contribution.

    - Authentication required
    - Only the contributor or admin can update
    - If updating task_id, task must belong to the contribution's project
    """
    is_admin = is_admin_user(current_user)

    return GitContributionService.update_contribution(
        db, contribution_id, contribution_in, current_user.id, is_admin
    )


@router.patch("/{contribution_id}/link-task", response_model=GitContribution)
def link_contribution_to_task(
    contribution_id: int,
    task_id: Optional[int] = Query(None, description="Task ID to link (null to unlink)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Link a contribution to a task.

    - Authentication required
    - Only the contributor or admin can link commits
    - Task must belong to the contribution's project
    """
    is_admin = is_admin_user(current_user)

    return GitContributionService.link_to_task(
        db, contribution_id, task_id, current_user.id, is_admin
    )
