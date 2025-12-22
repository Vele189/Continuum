# pylint: disable=unused-argument,redefined-outer-name
from typing import List, Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user, get_current_active_admin, is_admin_user
from app.dbmodels import User
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


@router.post("/", response_model=Project, status_code=status.HTTP_201_CREATED)
def create_project(
    project_in: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin),
):
    """
    Create a new project.
    
    Requires admin privileges (ADMIN or PROJECTMANAGER role).
    """
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
    
    - Admins see all projects
    - Regular users see only projects they are members of
    """
    is_admin = is_admin_user(current_user)

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
    
    - Admins can view any project
    - Members can only view projects they belong to
    """
    is_admin = is_admin_user(current_user)
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
    
    - Admins can update any project
    - Members can update projects they belong to
    """
    is_admin = is_admin_user(current_user)
    return ProjectService.update_project(
        db, project_id, project_in, current_user.id, is_admin=is_admin
    )


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin),
):
    """
    Delete a project.
    
    Requires admin privileges (ADMIN or PROJECTMANAGER role).
    """
    ProjectService.delete_project(db, project_id)


@router.post(
    "/{project_id}/members",
    response_model=ProjectMember,
    status_code=status.HTTP_201_CREATED
)
def add_member(
    project_id: int,
    member_in: ProjectMemberCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin),
):
    """
    Add a member to a project.
    
    Requires admin privileges (ADMIN or PROJECTMANAGER role).
    """
    return ProjectService.add_member(db, project_id, member_in)


@router.delete("/{project_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_member(
    project_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin),
):
    """
    Remove a member from a project.
    
    Requires admin privileges (ADMIN or PROJECTMANAGER role).
    """
    ProjectService.remove_member(db, project_id, user_id)


@router.get("/{project_id}/members", response_model=List[ProjectMember])
def get_members(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get project members.
    
    - Admins can view members of any project
    - Members can view members of projects they belong to
    """
    is_admin = is_admin_user(current_user)
    # Verify access to project first
    ProjectService.get_project_with_check(db, project_id, current_user.id, is_admin=is_admin)
    return ProjectService.list_members(db, project_id)
