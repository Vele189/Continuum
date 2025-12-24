from typing import Optional, List, Dict, Any
from datetime import datetime
from collections import defaultdict
import uuid
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.database import User, LoggedHour, GitContribution, ProjectMember, Project, UserRole
from app.schemas.user import UserCreate, UserUpdate, UserProfile, ProjectSummary
from fastapi import HTTPException


def get_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def create(db: Session, obj_in: UserCreate) -> User:
    verification_token = str(uuid.uuid4())
    db_obj = User(
        username=obj_in.email,
        display_name=f"{obj_in.first_name} {obj_in.last_name}",
        email=obj_in.email,
        hashed_password=hash_password(obj_in.password),
        first_name=obj_in.first_name,
        last_name=obj_in.last_name,
        role=obj_in.role,
        is_verified=False,
        verification_token=verification_token
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)

    # Mock sending email
    print("--- MOCK EMAIL ---")
    print("To: " + obj_in.email)
    print("Subject: Verify your email")
    print("Link: http://localhost:8000/api/v1/users/verify-email?token=" + verification_token)
    print("------------------")

    return db_obj

def authenticate(db: Session, email: str, password: str) -> Optional[User]:
    user = get_by_email(db, email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def update_refresh_token(db: Session, user: User, token: Optional[str]) -> User:
    user.refresh_token = token
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def verify_email(db: Session, token: str) -> Optional[User]:
    user = db.query(User).filter(User.verification_token == token).first()
    if not user:
        return None
    user.is_verified = True
    user.verification_token = None  # Clear token after use
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def initiate_password_reset(db: Session, email: str) -> Optional[User]:
    user = get_by_email(db, email=email)
    if not user:
        return None

    reset_token = str(uuid.uuid4())
    user.password_reset_token = reset_token
    db.add(user)
    db.commit()
    db.refresh(user)

    # Mock sending email
    print("--- MOCK EMAIL ---")
    print("To: " + email)
    print("Subject: Reset your password")
    print("Token: " + reset_token)
    print("------------------")

    return user

def reset_password(db: Session, token: str, new_password: str) -> Optional[User]:
    user = db.query(User).filter(User.password_reset_token == token).first()
    if not user:
        return None

    user.hashed_password = hash_password(new_password)
    user.password_reset_token = None  # Clear token
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_profile(db: Session, user: User, user_update: UserUpdate) -> User:
    """Update user profile with provided data"""
    update_data = user_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(user, field, value)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def change_password(
    db: Session,
    user: User,
    current_password: str,
    new_password: str
) -> Optional[User]:
    """Change user password after verifying current password"""
    # Verify current password
    if not verify_password(current_password, user.hashed_password):
        return None

    # Hash and update new password
    user.hashed_password = hash_password(new_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_profile(
    db: Session,
    user_id: int,
    current_user: User
) -> UserProfile:
    """
    Get comprehensive user profile including skills, contributions, and activity patterns.
    """
    # 1. Permission check
    admin_roles = {UserRole.ADMIN, UserRole.PROJECTMANAGER}
    if current_user.id != user_id and current_user.role not in admin_roles:
        raise HTTPException(status_code=403, detail="Not authorized to view this profile")
    
    # 2. Fetch user
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # 3. Aggregate logged hours
    total_hours = db.query(func.sum(LoggedHour.hours))\
        .filter(LoggedHour.user_id == user_id)\
        .scalar() or 0.0
    
    # 4. Aggregate git contributions
    total_commits = db.query(func.count(GitContribution.id))\
        .filter(GitContribution.user_id == user_id)\
        .scalar() or 0
    
    # 5. Count projects
    projects_count = db.query(func.count(func.distinct(ProjectMember.project_id)))\
        .filter(ProjectMember.user_id == user_id)\
        .scalar() or 0
    
    # 6. Compute activity patterns
    logged_hours_records = db.query(LoggedHour)\
        .filter(LoggedHour.user_id == user_id)\
        .all()
    
    hours_by_week = defaultdict(float)
    hours_by_month = defaultdict(float)
    day_counts = defaultdict(int)
    
    for log in logged_hours_records:
        # Week format: "2024-W01"
        week_key = log.date.strftime("%Y-W%U")
        hours_by_week[week_key] += log.hours
        
        # Month format: "2024-01"
        month_key = log.date.strftime("%Y-%m")
        hours_by_month[month_key] += log.hours
        
        # Day name
        day_name = log.date.strftime("%A")
        day_counts[day_name] += 1
    
    # Most active days (top 3)
    most_active_days = sorted(day_counts.items(), key=lambda x: x[1], reverse=True)[:3]
    most_active_days = [day for day, _ in most_active_days]
    
    # 7. Get projects worked on with specific details
    project_memberships = db.query(ProjectMember)\
        .filter(ProjectMember.user_id == user_id)\
        .all()
    
    projects_worked_on = []
    for pm in project_memberships:
        project = db.query(Project).filter(Project.id == pm.project_id).first()
        if project:
            # Calculate total hours for this specific user on this specific project
            project_hours = db.query(func.sum(LoggedHour.hours))\
                .filter(LoggedHour.user_id == user_id, LoggedHour.project_id == project.id)\
                .scalar() or 0.0
            
            projects_worked_on.append(ProjectSummary(
                id=project.id,
                name=project.name,
                role=pm.role,
                hours_logged=float(project_hours)
            ))
    
    # 8. Build response
    return UserProfile(
        id=user.id,
        name=user.display_name or f"{user.first_name} {user.last_name}",
        email=user.email,
        skills=user.skills if isinstance(user.skills, list) else [],
        contributions_summary={
            "total_logged_hours": float(total_hours),
            "total_commits": total_commits,
            "projects_count": projects_count
        },
        activity_patterns={
            "hours_by_week": dict(hours_by_week),
            "hours_by_month": dict(hours_by_month),
            "most_active_days": most_active_days
        },
        projects_worked_on=projects_worked_on
    )

