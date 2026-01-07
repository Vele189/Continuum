from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from fastapi import HTTPException, status

from app.dbmodels import WorkSession, WorkSessionStatus, LoggedHour, User
from app.schemas.work_session import WorkSessionCreate, WorkSessionUpdate

def get_active_session(db: Session, user_id: int) -> Optional[WorkSession]:
    """Return the current active or paused session for a user."""
    return db.query(WorkSession).filter(
        and_(
            WorkSession.user_id == user_id,
            WorkSession.status.in_([WorkSessionStatus.ACTIVE, WorkSessionStatus.PAUSED])
        )
    ).first()

def start_session(db: Session, user: User, data: WorkSessionCreate) -> WorkSession:
    """Start a new work session."""
    active = get_active_session(db, user.id)
    if active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already has an active or paused session"
        )
    
    now = datetime.now()
    db_session = WorkSession(
        user_id=user.id,
        project_id=data.project_id,
        task_id=data.task_id,
        note=data.note,
        started_at=now,
        last_resumed_at=now,
        duration_seconds=0,
        status=WorkSessionStatus.ACTIVE
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

def pause_session(db: Session, session_id: int, user: User) -> WorkSession:
    """Pause an active session."""
    session = db.query(WorkSession).filter(WorkSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    
    if session.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your session")
    
    if session.status != WorkSessionStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only active sessions can be paused"
        )
    
    now = datetime.now()
    if session.last_resumed_at:
        elapsed = int((now - session.last_resumed_at).total_seconds())
        session.duration_seconds += elapsed
    
    session.last_resumed_at = None
    session.status = WorkSessionStatus.PAUSED
    
    db.add(session)
    db.commit()
    db.refresh(session)
    return session

def resume_session(db: Session, session_id: int, user: User) -> WorkSession:
    """Resume a paused session."""
    session = db.query(WorkSession).filter(WorkSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    
    if session.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your session")
    
    if session.status != WorkSessionStatus.PAUSED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only paused sessions can be resumed"
        )
    
    session.last_resumed_at = datetime.now()
    session.status = WorkSessionStatus.ACTIVE
    
    db.add(session)
    db.commit()
    db.refresh(session)
    return session

def stop_session(db: Session, session_id: int, user: User) -> WorkSession:
    """Stop a session and create a LoggedHour entry."""
    session = db.query(WorkSession).filter(WorkSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    
    if session.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your session")
    
    if session.status not in [WorkSessionStatus.ACTIVE, WorkSessionStatus.PAUSED]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Session is already completed"
        )
    
    now = datetime.now()
    if session.status == WorkSessionStatus.ACTIVE and session.last_resumed_at:
        elapsed = int((now - session.last_resumed_at).total_seconds())
        session.duration_seconds += elapsed
    
    session.ended_at = now
    session.status = WorkSessionStatus.COMPLETED
    
    # Create LoggedHour
    hours = round(session.duration_seconds / 3600.0, 2)
    logged_hour = LoggedHour(
        user_id=user.id,
        project_id=session.project_id,
        task_id=session.task_id,
        hours=hours,
        note=session.note,
        logged_at=now
    )
    
    try:
        db.add(session)
        db.add(logged_hour)
        db.commit()
        db.refresh(session)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to stop session and log hours: {str(e)}"
        )
    
    return session

def list_sessions(
    db: Session, 
    user_id: int, 
    skip: int = 0, 
    limit: int = 100
) -> List[WorkSession]:
    """List session history for a user."""
    return db.query(WorkSession).filter(
        WorkSession.user_id == user_id
    ).order_by(WorkSession.started_at.desc()).offset(skip).limit(limit).all()
