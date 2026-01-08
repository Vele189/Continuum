from datetime import datetime, timezone
from typing import List, Optional

from app.api.deps import (
    get_current_active_admin,
    get_current_project_member,
    get_current_user,
    get_db,
    is_admin_user,
)
from app.dbmodels import User
from app.schemas.digest import WeeklyDigest
from app.schemas.milestone import Milestone
from app.schemas.project import (
    Project,
    ProjectCreate,
    ProjectDetail,
    ProjectHealth,
    ProjectMember,
    ProjectMemberCreate,
    ProjectStatistics,
    ProjectUpdate,
)
from app.schemas.summary import ProjectSummary
from app.services.digest import DigestService
from app.services.milestone import MilestoneService
from app.services.project import ProjectService
from app.services.summary import SummaryService
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/", response_model=Project, status_code=status.HTTP_201_CREATED)
def create_project(
    project_in: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    is_admin: User = Depends(get_current_active_admin),  # pylint: disable=unused-argument
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
        db, current_user.id, is_admin=is_admin, client_id=client_id, status_filter=status
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
    current_user: User = Depends(get_current_user),  # pylint: disable=unused-argument
    is_admin: User = Depends(get_current_active_admin),  # pylint: disable=unused-argument
):
    """
    Delete a project.

    Requires admin privileges (ADMIN or PROJECTMANAGER role).
    """
    ProjectService.delete_project(db, project_id)


@router.post(
    "/{project_id}/members", response_model=ProjectMember, status_code=status.HTTP_201_CREATED
)
def add_member(
    project_id: int,
    member_in: ProjectMemberCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin),  # pylint: disable=unused-argument
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
    current_user: User = Depends(get_current_active_admin),  # pylint: disable=unused-argument
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


# we make a get requests endpoint for the project statistics
@router.get("/{project_id}/stats", response_model=ProjectStatistics)
def get_project_stats(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # pylint: disable=unused-argument
    member: ProjectMember = Depends(get_current_project_member),  # pylint: disable=unused-argument
):
    """
    Get project statistics.

    - Members can view stats of projects they belong to
    """
    return ProjectService.get_project_statistics(db=db, project_id=project_id)


# we make a get requests endpoint for the project health
@router.get("/{project_id}/health", response_model=ProjectHealth)
def get_project_health(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # pylint: disable=unused-argument
    member: ProjectMember = Depends(get_current_project_member),  # pylint: disable=unused-argument
):
    """
    Get project health.

    - Members can view health of projects they belong to
    """
    return ProjectService.get_project_health(db=db, project_id=project_id)


@router.get("/{project_id}/milestones", response_model=List[Milestone])
def list_project_milestones(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    List milestones for a project.

    - Admins can view milestones of any project
    - Members can view milestones of projects they belong to
    """
    is_admin = is_admin_user(current_user)
    # Verify access to project first
    ProjectService.get_project_with_check(db, project_id, current_user.id, is_admin=is_admin)

    milestones = MilestoneService.get_by_project(db, project_id)

    # Enrichment with progress
    results = []
    for m in milestones:
        MilestoneService.update_status(db, m)
        progress = MilestoneService.calculate_progress(db, m.id)

        # Pydantic model conversion
        # We need to construct the response manually to inject progress, or rely on pydantic validtion if property set
        # Since 'm' is SQLAlchemy model, we can attach the dict but pydantic v2 is stricter.
        # But 'Milestone' schema has 'progress' field.

        res = Milestone.model_validate(m)
        res.progress = progress
        results.append(res)

    return results


@router.get("/{project_id}/digest", response_model=WeeklyDigest)
def get_project_digest(
    project_id: int,
    week_start: datetime = Query(..., description="Start of the week (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Generate a weekly digest for a project.

    - Admins can view digest of any project
    - Members can view digest of projects they belong to
    """
    is_admin = is_admin_user(current_user)
    # Verify access to project
    ProjectService.get_project_with_check(db, project_id, current_user.id, is_admin=is_admin)

    return DigestService.generate_weekly_digest(db, project_id, week_start)


@router.post("/{project_id}/generate-summary", response_model=ProjectSummary)
def generate_project_summary(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Generate a structured project summary aggregating tasks, commits, and logged hours.
    Used as input for future AI processing.

    - Admins can generate summary for any project
    - Members can generate summary for projects they belong to
    """
    is_admin = is_admin_user(current_user)
    # Verify access to project
    ProjectService.get_project_with_check(db, project_id, current_user.id, is_admin=is_admin)

    summary_data = SummaryService.generate_project_summary(db, project_id)
    summary_data["generated_at"] = datetime.now(timezone.utc)

    return summary_data
