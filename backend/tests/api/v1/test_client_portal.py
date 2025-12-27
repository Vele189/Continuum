from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.dbmodels import User, UserRole, Project, Client, ProjectMember
from app.core.config import settings

def test_client_portal_project_read(client: TestClient):
    # 1. Setup: Create User, Client, Project, and Member
    db = SessionLocal()
    
    # Create a user to be a project member
    user = User(
        email="member@test.com",
        username="member",
        display_name="Member User",
        first_name="John",
        last_name="Doe",
        hashed_password="hashed"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Create a client with api_key
    portal_client = Client(
        name="Portal Client",
        api_key="client-portal-token"
    )
    db.add(portal_client)
    db.commit()
    db.refresh(portal_client)
    
    # Create a project for this client
    project = Project(
        name="Client Visible Project",
        description="This project is visible to the client.",
        client_id=portal_client.id,
        status="active"
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    
    # Add the user as a member
    member = ProjectMember(
        project_id=project.id,
        user_id=user.id,
        role="developer"
    )
    db.add(member)
    db.commit()
    
    project_id = project.id
    db.close()
    
    # 2. Test: Successful Read
    response = client.get(
        f"{settings.API_V1_STR}/client-portal/projects/{project_id}",
        headers={"X-Client-Token": "client-portal-token"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Client Visible Project"
    assert data["client_name"] == "Portal Client"
    assert "John Doe" in data["members"]
    assert "updated_at" in data
    
    # 3. Test: Unauthorized (invalid token)
    response = client.get(
        f"{settings.API_V1_STR}/client-portal/projects/{project_id}",
        headers={"X-Client-Token": "wrong-token"}
    )
    assert response.status_code == 401
    
    # 4. Test: Unauthorized (missing token)
    response = client.get(
        f"{settings.API_V1_STR}/client-portal/projects/{project_id}"
    )
    assert response.status_code == 401
    
    # 5. Test: Forbidden (accessing another client's project)
    db = SessionLocal()
    other_client = Client(name="Other Client", api_key="other-token")
    db.add(other_client)
    db.commit()
    db.refresh(other_client)
    db.close()
    
    response = client.get(
        f"{settings.API_V1_STR}/client-portal/projects/{project_id}",
        headers={"X-Client-Token": "other-token"}
    )
    assert response.status_code == 403

def test_client_portal_sanitization(client: TestClient):
    db = SessionLocal()
    portal_client = Client(name="Sanity Client", api_key="sanity-token")
    db.add(portal_client)
    db.commit()
    db.refresh(portal_client)
    
    project = Project(
        name="Secrets Project",
        client_id=portal_client.id
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    project_id = project.id
    db.close()
    
    response = client.get(
        f"{settings.API_V1_STR}/client-portal/projects/{project_id}",
        headers={"X-Client-Token": "sanity-token"}
    )
    assert response.status_code == 200
    data = response.json()
    
    # Positive checks
    assert "id" in data
    assert "name" in data
    assert "status" in data
    
    # Negative checks (ensure excluded fields are not present)
    assert "client_id" not in data
    assert "tasks" not in data
    assert "logged_hours" not in data
    assert "hourly_rate" not in data
