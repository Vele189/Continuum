from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user, get_current_active_admin
from app.database import User, UserRole
from app.schemas.project import (
    Project,
    ProjectCreate, 
    ProjectUpdate, 
    ProjectMember, 
    ProjectMemberCreate,
    ProjectDetail
)
from app.services.project import ProjectService

router = APIRouter()

@router.post("/", response_model=Project)
def create_project(
    project_in: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new project.
    """
    is_admin = current_user.role == UserRole.CLIENT
    if not is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can create projects")
        
    return ProjectService.create_project(db, project_in, current_user.id)

@router.get("/", response_model=List[Project])
def list_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    client_id: Optional[int] = Query(None, description="Filter by client ID"),
    status: Optional[str] = Query(None, description="Filter by status"),
):
    """
    List projects. 
    Returns all projects for admins, or only member-projects for regular users.
    """
    is_admin = current_user.role == UserRole.CLIENT
    
    return ProjectService.list_projects(
        db, 
        current_user.id, 
        is_admin=is_admin,
        client_id=client_id, 
        status_filter=status
    )

@router.get("/{project_id}", response_model=ProjectDetail)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get project by ID.
    Members can view.
    """
    is_admin = current_user.role == UserRole.CLIENT
    return ProjectService.get_project_with_check(db, project_id, current_user.id, is_admin=is_admin)

@router.put("/{project_id}", response_model=Project)
def update_project(
    project_id: int,
    project_in: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update project.
    Members can update allowed fields.
    """
    is_admin = current_user.role == UserRole.CLIENT
    return ProjectService.update_project(db, project_id, project_in, current_user.id, is_admin=is_admin)

@router.delete("/{project_id}", response_model=Project)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Delete a project.
    This is for an Admin only(So only an admin can delete a project).
    """
    is_admin = current_user.role == UserRole.CLIENT
    return ProjectService.delete_project(db, project_id, current_user.id, is_admin=is_admin)

@router.post("/{project_id}/members", response_model=ProjectMember)
def add_member(
    project_id: int,
    member_in: ProjectMemberCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Add a member to a project.
    """
    is_admin = current_user.role == UserRole.CLIENT
    
    if not is_admin:
        raise HTTPException(status_code=403, detail="Only admins can add members")

    return ProjectService.add_member(db, project_id, member_in)

@router.delete("/{project_id}/members/{user_id}", response_model=ProjectMember)
def remove_member(
    project_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Remove a member from a project.
    """
    is_admin = current_user.role == UserRole.CLIENT
    if not is_admin:
        raise HTTPException(status_code=403, detail="Only admins can remove members")
        
    return ProjectService.remove_member(db, project_id, user_id)

@router.get("/{project_id}/members", response_model=List[ProjectMember])
def get_members(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get project members.
    """
    is_admin = current_user.role == UserRole.CLIENT
    # Check access to project first?
    try:
        ProjectService.get_project_with_check(db, project_id, current_user.id, is_admin=is_admin)
    except HTTPException:
        raise # This will PROBABLY raise 403 or 404
        
    return ProjectService.list_members(db, project_id)
