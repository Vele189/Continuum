from datetime import datetime, timedelta

from app.core.config import settings
from app.dbmodels import GitContribution, LoggedHour, Project, ProjectMember, Task, User
from app.schemas.user import UserRole
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def test_get_project_digest_successful(client: TestClient, db: Session):
    # 1. Setup Data
    # Create a user/admin
    admin_user = User(
        email="admin@test.com",
        username="admin",
        display_name="Admin User",
        first_name="Admin",
        last_name="User",
        hashed_password="hashed_password",
        role=UserRole.ADMIN,
    )
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)

    # Login and get token (we'll use a mocked/fixed token if auth is mocked in conftest,
    # but here we'll assume we need to authenticate or use the client fixture)
    # The 'client' fixture in conftest.py usually handles the app setup.
    # We might need to mock get_current_user or similar.

    # Create a project
    project = Project(
        name="Test Project",
        client_id=1,  # Assuming client 1 exists or created
    )
    db.add(project)
    db.commit()
    db.refresh(project)

    # Add member
    member = ProjectMember(project_id=project.id, user_id=admin_user.id, role="admin")
    db.add(member)
    db.commit()

    # Create activity within "this week"
    week_start = datetime(2023, 10, 1)  # Example date
    activity_date = week_start + timedelta(days=2)

    # 1 Task completed
    task = Task(
        project_id=project.id, title="Completed Task", status="completed", updated_at=activity_date
    )
    db.add(task)

    # 5 Hours logged
    logged_hour = LoggedHour(
        user_id=admin_user.id,
        project_id=project.id,
        task_id=None,
        hours=5.0,
        logged_at=activity_date,
    )
    db.add(logged_hour)

    # 1 Git contribution
    contribution = GitContribution(
        user_id=admin_user.id,
        project_id=project.id,
        commit_hash="abc123hash",
        commit_message="Initial commit",
        provider="github",
        created_at=activity_date,
    )
    db.add(contribution)
    db.commit()

    # 2. Get Digest
    # Mock authentication by passing dependencies if needed,
    # but since we are using TestClient, we'll override get_current_user
    from app.api.deps import get_current_user

    app = client.app
    app.dependency_overrides[get_current_user] = lambda: admin_user

    response = client.get(
        f"{settings.API_V1_STR}/projects/{project.id}/digest", params={"week_start": "2023-10-01"}
    )

    # 3. Assertions
    assert response.status_code == 200
    data = response.json()
    assert data["project_id"] == project.id
    assert data["project_name"] == project.name
    assert data["total_hours_logged"] == 5.0
    assert len(data["completed_tasks"]) == 1
    assert data["completed_tasks"][0]["title"] == "Completed Task"
    assert len(data["commits"]) == 1
    assert data["commits"][0]["hash"] == "abc123hash"
    assert data["risks_and_delays"][0]["reason"] == "Risk detection not implemented yet"

    # Cleanup overrides
    app.dependency_overrides = {}


def test_get_project_digest_forbidden(client: TestClient, db: Session):
    # Setup two users
    user1 = User(
        email="user1@test.com",
        username="user1",
        display_name="User 1",
        first_name="U1",
        last_name="S1",
        hashed_password="pw",
        role=UserRole.BACKEND,
    )
    user2 = User(
        email="user2@test.com",
        username="user2",
        display_name="User 2",
        first_name="U2",
        last_name="S2",
        hashed_password="pw",
        role=UserRole.BACKEND,
    )
    db.add(user1)
    db.add(user2)
    db.commit()

    # Project for user 1
    project = Project(name="User 1 Project", client_id=1)
    db.add(project)
    db.commit()
    db.refresh(project)

    member = ProjectMember(project_id=project.id, user_id=user1.id, role="member")
    db.add(member)
    db.commit()

    # User 2 tries to access User 1's digest
    from app.api.deps import get_current_user

    app = client.app
    app.dependency_overrides[get_current_user] = lambda: user2

    response = client.get(
        f"{settings.API_V1_STR}/projects/{project.id}/digest", params={"week_start": "2023-10-01"}
    )

    assert response.status_code == 403
    app.dependency_overrides = {}
