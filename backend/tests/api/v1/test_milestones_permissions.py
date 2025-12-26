from app.core.config import settings
from app.db.session import SessionLocal
from app.dbmodels import Client, Project, ProjectMember, User, UserRole
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def create_user_and_token(client: TestClient, email: str, role: UserRole):
    # Create user via API to get default setup
    user_data = {
        "email": email,
        "password": "password123",
        "first_name": "Test",
        "last_name": role.value,
        "username": email.split("@")[0],
        "display_name": "Test User",
    }
    client.post(f"{settings.API_V1_STR}/users/", json=user_data)

    # Update role manually
    db = SessionLocal()
    user = db.query(User).filter(User.email == email).first()
    if user:
        user.role = role
        db.add(user)
        db.commit()
    db.close()

    # Login
    login_data = {
        "username": email,  # OAuth2PasswordRequestForm uses username field for email
        "password": "password123",
    }
    # Try login endpoint
    response = client.post(f"{settings.API_V1_STR}/auth/login/access-token", data=login_data)
    if response.status_code != 200:
        # Fallback for some auth setups
        response = client.post(
            f"{settings.API_V1_STR}/auth/login", json={"email": email, "password": "password123"}
        )

    return response.json()["access_token"]


def setup_project(db: Session, owner_email: str):
    user = db.query(User).filter(User.email == owner_email).first()

    # Create Client
    client = Client(name="Test Client", created_by=user.id)
    db.add(client)
    db.commit()
    db.refresh(client)

    # Create Project
    project = Project(name="Test Project", client_id=client.id, status="active")
    db.add(project)
    db.commit()
    db.refresh(project)

    return project


def add_member(db: Session, project_id: int, user_email: str):
    user = db.query(User).filter(User.email == user_email).first()
    member = ProjectMember(project_id=project_id, user_id=user.id)
    db.add(member)
    db.commit()


def test_milestone_permissions(client: TestClient):
    # Setup Users
    admin_token = create_user_and_token(client, "admin@test.com", UserRole.ADMIN)
    member_token = create_user_and_token(client, "member@test.com", UserRole.BACKEND)
    outsider_token = create_user_and_token(client, "outsider@test.com", UserRole.FRONTEND)

    db = SessionLocal()
    project = setup_project(db, "admin@test.com")
    add_member(db, project.id, "member@test.com")
    project_id = project.id
    db.close()

    # 1. Admin Create Milestone - OK
    milestone_data = {
        "name": "Admin Milestone",
        "project_id": project_id,
        "due_date": "2025-12-31T23:59:59Z",
    }
    response = client.post(
        f"{settings.API_V1_STR}/milestones/",
        json=milestone_data,
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 201
    milestone_id = response.json()["id"]

    # 2. Member Create Milestone - Forbidden
    response = client.post(
        f"{settings.API_V1_STR}/milestones/",
        json={"name": "Member Milestone", "project_id": project_id},
        headers={"Authorization": f"Bearer {member_token}"},
    )
    assert response.status_code == 403

    # 3. Member List Milestones - OK
    response = client.get(
        f"{settings.API_V1_STR}/milestones/?project_id={project_id}",
        headers={"Authorization": f"Bearer {member_token}"},
    )
    assert response.status_code == 200
    assert len(response.json()) >= 1

    # 4. Outsider List Milestones - Forbidden
    response = client.get(
        f"{settings.API_V1_STR}/milestones/?project_id={project_id}",
        headers={"Authorization": f"Bearer {outsider_token}"},
    )
    # The get_project_with_check raises 403 if not member
    assert response.status_code == 403

    # 5. Admin Update Milestone - OK
    response = client.put(
        f"{settings.API_V1_STR}/milestones/{milestone_id}",
        json={"name": "Updated Name"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Name"

    # 6. Member Update Milestone - Forbidden
    response = client.put(
        f"{settings.API_V1_STR}/milestones/{milestone_id}",
        json={"name": "Hacked Name"},
        headers={"Authorization": f"Bearer {member_token}"},
    )
    assert response.status_code == 403

    # 7. Get Milestone - Outsider Forbidden
    response = client.get(
        f"{settings.API_V1_STR}/milestones/{milestone_id}",
        headers={"Authorization": f"Bearer {outsider_token}"},
    )
    # Depending on implementation order, could be 403 (project check) or 404
    assert response.status_code == 403

    # 8. Get Milestone - Member OK
    response = client.get(
        f"{settings.API_V1_STR}/milestones/{milestone_id}",
        headers={"Authorization": f"Bearer {member_token}"},
    )
    assert response.status_code == 200

    # 9. Admin Delete Milestone - OK
    response = client.delete(
        f"{settings.API_V1_STR}/milestones/{milestone_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 204

    # 10. Member Delete Milestone (create another one first) - Forbidden
    # Admin creates another one
    res = client.post(
        f"{settings.API_V1_STR}/milestones/",
        json={"name": "To Delete", "project_id": project_id},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    mid_2 = res.json()["id"]

    response = client.delete(
        f"{settings.API_V1_STR}/milestones/{mid_2}",
        headers={"Authorization": f"Bearer {member_token}"},
    )
    assert response.status_code == 403


def test_list_milestones_filter_status(client: TestClient):
    # Setup
    admin_token = create_user_and_token(client, "admin_filter@test.com", UserRole.ADMIN)
    db = SessionLocal()
    project = setup_project(db, "admin_filter@test.com")
    project_id = project.id
    db.close()

    # Create milestones with different statuses
    m1 = {
        "name": "M1",
        "project_id": project_id,
        "due_date": "2025-12-31T23:59:59Z",  # Status: not_started (default)
    }
    client.post(
        f"{settings.API_V1_STR}/milestones/",
        json=m1,
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    # We need to manually update status in DB or simulate it,
    # but currently service auto-updates status on read.
    # To test 'completed', we need tasks. To test 'overdue', we need past date.

    # Overdue Milestone
    m2 = {"name": "M2 Overdue", "project_id": project_id, "due_date": "2020-01-01T00:00:00Z"}
    client.post(
        f"{settings.API_V1_STR}/milestones/",
        json=m2,
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    # Filter 'not_started'
    response = client.get(
        f"{settings.API_V1_STR}/milestones/?project_id={project_id}&status=not_started",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert all(m["status"] == "not_started" for m in data)

    # Filter 'overdue'
    # Note: Status update happens on read. When we list with filter,
    # we first query DB (old status) -> then update.
    # So if the status wasn't 'overdue' in DB yet, it might not return if we filter by SQL.
    # The current implementation filters in SQL `query.filter(Milestone.status == status)`.
    # BUT `MilestoneService.update_status` is called AFTER fetching in the loop.
    # This means filters apply to "stale" status.
    # We need to trigger an update first or accept that filters apply to stored status.

    # Let's force an update by reading individual milestones first

    # Get all to trigger updates
    client.get(
        f"{settings.API_V1_STR}/milestones/?project_id={project_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    # Now filter should work
    response = client.get(
        f"{settings.API_V1_STR}/milestones/?project_id={project_id}&status=overdue",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    # M2 should be overdue now
    assert len(data) >= 1
    assert all(m["status"] == "overdue" for m in data)
