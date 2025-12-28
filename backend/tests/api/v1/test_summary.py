from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.dbmodels import User, Project, Task, LoggedHour, GitContribution, ProjectMember
from app.schemas.user import UserRole


def test_generate_project_summary_successful(client: TestClient, db: Session):
    # 1. Setup Data
    # Create an admin user
    admin_user = User(
        email="admin_summary@test.com",
        username="admin_summary",
        display_name="Admin Summary",
        first_name="Admin",
        last_name="Summary",
        hashed_password="hashed_password",
        role=UserRole.ADMIN
    )
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)

    # Overwrite auth
    from app.api.deps import get_current_user
    app = client.app
    app.dependency_overrides[get_current_user] = lambda: admin_user

    # Create a project
    project = Project(
        name="Summary Test Project",
        client_id=1,
    )
    db.add(project)
    db.commit()
    db.refresh(project)

    # Add member
    member = ProjectMember(
        project_id=project.id,
        user_id=admin_user.id,
        role="admin"
    )
    db.add(member)

    # Create activity
    # 1 Task with description
    task = Task(
        project_id=project.id,
        title="Summary Task",
        description="This is a test task description.",
        status="done"
    )
    db.add(task)

    # 1 Git contribution
    contribution = GitContribution(
        user_id=admin_user.id,
        project_id=project.id,
        commit_hash="summaryhash123",
        commit_message="Documentation update",
        provider="github"
    )
    db.add(contribution)

    # 1 Logged hour
    logged_hour = LoggedHour(
        user_id=admin_user.id,
        project_id=project.id,
        hours=2.5,
        note="Writing tests for summary feature"
    )
    db.add(logged_hour)
    db.commit()

    # 2. Call Endpoint
    response = client.post(
        f"{settings.API_V1_STR}/projects/{project.id}/generate-summary"
    )

    # 3. Assertions
    assert response.status_code == 200
    data = response.json()
    assert data["project_id"] == project.id
    assert data["project_name"] == "Summary Test Project"
    assert "This is a test task description." in data["task_descriptions"]
    assert "Documentation update" in data["commit_messages"]
    assert "Writing tests for summary feature" in data["logged_hour_notes"]
    assert "### Task Descriptions" in data["aggregated_text"]
    assert data["metadata"]["total_tasks"] == 1
    assert data["metadata"]["total_commits"] == 1
    assert data["metadata"]["total_logged_hours"] == 2 # int(2.5)
    assert data["metadata"]["task_count_by_status"]["done"] == 1
    assert "generated_at" in data

    # Cleanup
    app.dependency_overrides = {}


def test_generate_project_summary_forbidden(client: TestClient, db: Session):
    # Setup two users
    user1 = User(
        email="u1_summary@test.com", username="u1_s", display_name="U1 S",
        first_name="U1", last_name="S1", hashed_password="pw", role=UserRole.BACKEND
    )
    user2 = User(
        email="u2_summary@test.com", username="u2_s", display_name="U2 S",
        first_name="U2", last_name="S2", hashed_password="pw", role=UserRole.BACKEND
    )
    db.add(user1)
    db.add(user2)
    db.commit()

    # Project for user 1
    project = Project(name="U1 Project", client_id=1)
    db.add(project)
    db.commit()
    db.refresh(project)

    member = ProjectMember(project_id=project.id, user_id=user1.id, role="member")
    db.add(member)
    db.commit()

    # User 2 tries to access User 1's summary
    from app.api.deps import get_current_user
    app = client.app
    app.dependency_overrides[get_current_user] = lambda: user2

    response = client.post(
        f"{settings.API_V1_STR}/projects/{project.id}/generate-summary"
    )

    assert response.status_code == 403
    app.dependency_overrides = {}


def test_generate_project_summary_null_handling(client: TestClient, db: Session):
    # Setup
    admin_user = User(
        email="admin_null@test.com", username="admin_null", role=UserRole.ADMIN,
        hashed_password="pw", first_name="A", last_name="N", display_name="Admin Null"
    )
    db.add(admin_user)
    db.commit()

    project = Project(name="Null Test Project", client_id=1)
    db.add(project)
    db.commit()

    # Add activity with null/empty content
    db.add(Task(project_id=project.id, title="T1", description=None, status="todo"))
    db.add(Task(project_id=project.id, title="T2", description="", status="todo"))
    db.add(Task(project_id=project.id, title="T3", description="  ", status="todo"))
    db.add(Task(project_id=project.id, title="T4", description="Valid", status="todo"))

    db.add(GitContribution(
        user_id=admin_user.id, project_id=project.id, commit_hash="h1",
        commit_message=None, provider="github"
    ))
    db.add(GitContribution(
        user_id=admin_user.id, project_id=project.id, commit_hash="h2",
        commit_message="Valid Commit", provider="github"
    ))

    db.add(LoggedHour(
        user_id=admin_user.id, project_id=project.id, hours=1.0, note=""
    ))
    db.add(LoggedHour(
        user_id=admin_user.id, project_id=project.id, hours=1.0, note="Valid Note"
    ))
    db.commit()

    from app.api.deps import get_current_user
    client.app.dependency_overrides[get_current_user] = lambda: admin_user

    response = client.post(f"{settings.API_V1_STR}/projects/{project.id}/generate-summary")
    assert response.status_code == 200
    data = response.json()

    # Assertions
    assert len(data["task_descriptions"]) == 1
    assert data["task_descriptions"][0] == "Valid"
    assert len(data["commit_messages"]) == 1
    assert data["commit_messages"][0] == "Valid Commit"
    assert len(data["logged_hour_notes"]) == 1
    assert data["logged_hour_notes"][0] == "Valid Note"
    
    # Metadata should still count them
    assert data["metadata"]["total_tasks"] == 4
    assert data["metadata"]["total_commits"] == 2
    assert data["metadata"]["total_logged_hours"] == 2

    client.app.dependency_overrides = {}
