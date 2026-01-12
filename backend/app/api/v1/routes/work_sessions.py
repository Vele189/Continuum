from typing import List, Optional

from app.api import deps
from app.dbmodels import User
from app.schemas.work_session import WorkSessionAction, WorkSessionCreate, WorkSessionOut
from app.services import work_session as work_session_service
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/", response_model=WorkSessionOut, status_code=status.HTTP_201_CREATED)
def start_session(
    data: WorkSessionCreate,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    """Start a new work session."""
    return work_session_service.start_session(db, user=current_user, data=data)


@router.get("/active", response_model=Optional[WorkSessionOut])
def get_active_session(
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    """Get the current active or paused session."""
    return work_session_service.get_active_session(db, user_id=current_user.id)


@router.post("/{id}/pause", response_model=WorkSessionOut)
def pause_session(
    id: int,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    """Pause an active session."""
    return work_session_service.pause_session(db, session_id=id, user=current_user)


@router.post("/{id}/resume", response_model=WorkSessionOut)
def resume_session(
    id: int,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    """Resume a paused session."""
    return work_session_service.resume_session(db, session_id=id, user=current_user)


@router.post("/{id}/stop", response_model=WorkSessionOut)
def stop_session(
    id: int,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    """Stop a session and log hours."""
    return work_session_service.stop_session(db, session_id=id, user=current_user)


@router.get("/", response_model=List[WorkSessionOut])
def list_sessions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    """List session history for the current user."""
    return work_session_service.list_sessions(db, user_id=current_user.id, skip=skip, limit=limit)
