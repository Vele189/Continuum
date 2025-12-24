
from typing import Optional, List, Dict 
import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from app.core.security import hash_password, verify_password
from app.dbmodels import User, ProjectMember, Project, LoggedHour
from app.schemas.user import UserCreate, UserUpdate, UserProjects, UserProject, UserHoursResponse, ProjectHours
from app.schemas.project import ProjectStatus
from collections import defaultdict
from sqlalchemy import func

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

def get_user_projects(db: Session, user: User) -> UserProjects:
    """Get all projects the user is a member of with their id, name, roles and project status"""
    
    user_projects = db.query(ProjectMember).filter(ProjectMember.user_id == user.id).all()
    
    
    projects_list = [
        UserProject(
            project_id=membership.project_id,
            name=membership.project.name,
            role=membership.role,
            status=membership.project.status
        )
        for membership in user_projects
    ]
    
    return UserProjects(projects=projects_list)


def get_user_hours(
    db: Session,
    user: User,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> UserHoursResponse:
    """
    Get all logged hours for a user, grouped by project.
    Optionally filter by date range.
    """
    # Get all projects the user is a member of
    memberships = (
        db.query(ProjectMember)
        .join(Project, ProjectMember.project_id == Project.id)
        .filter(ProjectMember.user_id == user.id)
        .all()
    )

    total_hours = 0.0
    projects_list = []

    for membership in memberships:
        # Query total hours for this user and project
        hours_query = db.query(func.sum(LoggedHour.hours)).filter(
            LoggedHour.project_id == membership.project_id,
            LoggedHour.user_id == user.id
        )

        # Apply date filters if provided
        if start_date:
            hours_query = hours_query.filter(LoggedHour.date >= start_date)
        if end_date:
            hours_query = hours_query.filter(LoggedHour.date <= end_date)

        project_hours = hours_query.scalar() or 0.0
        
        # Include all projects the user is a member of, even those with 0 hours
        projects_list.append(
            ProjectHours(
                project_id=membership.project_id,
                project_name=membership.project.name,
                total_hours=float(project_hours)
            )
        )
        total_hours += float(project_hours)

    # Sort projects by total hours (descending)
    projects_list.sort(key=lambda p: p.total_hours, reverse=True)

    return UserHoursResponse(
        total_hours=total_hours,
        projects=projects_list
    )
