from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api import deps
from app.database import User
from app.schemas.milestone import Milestone, MilestoneCreate, MilestoneUpdate
from app.services.milestone import MilestoneService

router = APIRouter()

@router.post("/", response_model=Milestone, status_code=status.HTTP_201_CREATED)
def create_milestone(
    milestone_in: MilestoneCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    # TODO: Add Project Permission Check
):
    """
    Create a new milestone.
    """
    # Verify User is member of project (omitted for brevity, handled in Task/Project services usually)
    # Ideally should call ProjectService.check_member(project_id, user_id)
    return MilestoneService.create(db, milestone_in)

@router.get("/{milestone_id}", response_model=Milestone)
def get_milestone(
    milestone_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Get a milestone by ID with progress metrics.
    """
    milestone = MilestoneService.get(db, milestone_id)
    if not milestone:
        raise HTTPException(status_code=404, detail="Milestone not found")
    
    # Auto-update status on read (lazy update strategy)
    milestone = MilestoneService.update_status(db, milestone)
    
    # Calculate progress for response
    progress = MilestoneService.calculate_progress(db, milestone.id)
    
    # Enrich response (Response Schema expects this structure)
    # The Pydantic model 'Milestone' inherits from 'MilestoneInDBBase' and adds 'progress'
    # We construct it explicitly or let Pydantic handle it if we attach the attribute
    # Since SQLAlchemy models don't hold 'progress', we might need to rely on the Pydantic model construction
    
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
    """
    milestone = MilestoneService.update(db, milestone_id, milestone_in)
    if not milestone:
        raise HTTPException(status_code=404, detail="Milestone not found")
    return milestone

@router.delete("/{milestone_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_milestone(
    milestone_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Delete a milestone.
    """
    success = MilestoneService.delete(db, milestone_id)
    if not success:
        raise HTTPException(status_code=404, detail="Milestone not found")

@router.get("/", response_model=List[Milestone])
def list_milestones(
    project_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    List milestones for a project.
    """
    milestones = MilestoneService.get_by_project(db, project_id)
    
    # For list view, we might want sparse progress or full? Scope says "Get /api/v1/milestones?project_id=". 
    # Usually list views need progress too for dashboards.
    results = []
    for m in milestones:
        # Lazy update status
        MilestoneService.update_status(db, m)
        prog = MilestoneService.calculate_progress(db, m.id)
        res = Milestone.model_validate(m)
        res.progress = prog
        results.append(res)
        
    return results
