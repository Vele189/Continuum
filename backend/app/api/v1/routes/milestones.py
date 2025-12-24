from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api import deps
from app.api.deps import is_admin_user
from app.dbmodels import User
from app.schemas.milestone import Milestone, MilestoneCreate, MilestoneUpdate
from app.services.milestone import MilestoneService
from app.services.project import ProjectService

router = APIRouter()

@router.post("/", response_model=Milestone, status_code=status.HTTP_201_CREATED)
def create_milestone(
    milestone_in: MilestoneCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Create a new milestone.

    Requires Admin or Project Manager privileges.
    """
    # Verify permissions: Admin or Project Owner
    is_admin = is_admin_user(current_user)
    is_owner = ProjectService.is_project_owner(db, milestone_in.project_id, current_user.id)

    if not (is_admin or is_owner):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to create milestones"
        )

    # Verify Project Exists (already checked in is_project_owner or handled by get_project_with_check)
    # But we call get_project_with_check to ensure consistency and membership logging if needed
    ProjectService.get_project_with_check(
        db, milestone_in.project_id, current_user.id, is_admin=is_admin
    )

    created_milestone = MilestoneService.create(db, milestone_in)

    # Calculate progress for response (same as GET endpoint)
    progress = MilestoneService.calculate_progress(db, created_milestone.id)

    response = Milestone.model_validate(created_milestone)
    response.progress = progress
    return response

@router.get("/{milestone_id}", response_model=Milestone)
def get_milestone(
    milestone_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Get a milestone by ID with progress metrics.

    Requires project membership (or admin).
    """
    milestone = MilestoneService.get(db, milestone_id)
    if not milestone:
        raise HTTPException(status_code=404, detail="Milestone not found")

    # Verify Project Membership
    is_admin = is_admin_user(current_user)
    ProjectService.get_project_with_check(
        db, milestone.project_id, current_user.id, is_admin=is_admin
    )

    # Auto-update status on read (lazy update strategy)
    milestone = MilestoneService.update_status(db, milestone)

    # Calculate progress for response
    progress = MilestoneService.calculate_progress(db, milestone.id)

    response = Milestone.model_validate(milestone)
    response.progress = progress
    return response

@router.put("/{milestone_id}", response_model=Milestone)
def update_milestone(
    milestone_id: int,
    milestone_in: MilestoneUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Update a milestone.

    Requires Admin or Project Manager privileges.
    """
    milestone = MilestoneService.get(db, milestone_id)
    if not milestone:
        raise HTTPException(status_code=404, detail="Milestone not found")

    # Verify permissions: Admin or Project Owner
    is_admin = is_admin_user(current_user)
    is_owner = ProjectService.is_project_owner(db, milestone.project_id, current_user.id)

    if not (is_admin or is_owner):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to update milestones"
        )

    updated_milestone = MilestoneService.update(db, milestone_id, milestone_in)

    # Calculate progress for response (same as GET endpoint)
    progress = MilestoneService.calculate_progress(db, updated_milestone.id)

    response = Milestone.model_validate(updated_milestone)
    response.progress = progress
    return response

@router.delete("/{milestone_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_milestone(
    milestone_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Delete a milestone.

    Requires Admin or Project Manager privileges.
    """
    milestone = MilestoneService.get(db, milestone_id)
    if not milestone:
        raise HTTPException(status_code=404, detail="Milestone not found")

    # Verify permissions: Admin or Project Owner
    is_admin = is_admin_user(current_user)
    is_owner = ProjectService.is_project_owner(db, milestone.project_id, current_user.id)

    if not (is_admin or is_owner):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to delete milestones"
        )

    success = MilestoneService.delete(db, milestone_id)
    if not success:
        raise HTTPException(status_code=404, detail="Milestone not found")

@router.get("/", response_model=List[Milestone])
def list_milestones(
    project_id: int,
    status: Optional[str] = Query(
        None,
        description="Filter by status (not_started, in_progress, completed, overdue)"
    ),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    List milestones for a project.

    Requires project membership (or admin).
    """
    # Verify Project Membership
    is_admin = is_admin_user(current_user)
    ProjectService.get_project_with_check(
        db, project_id, current_user.id, is_admin=is_admin
    )

    milestones = MilestoneService.get_by_project(db, project_id) # Get all to ensure status updates

    results = []
    for m in milestones:
        # Lazy update status
        updated_milestone = MilestoneService.update_status(db, m)

        # Apply filter here, after update
        if status and updated_milestone.status != status:
            continue

        prog = MilestoneService.calculate_progress(db, m.id)
        res = Milestone.model_validate(m)
        res.progress = prog
        results.append(res)

    return results
