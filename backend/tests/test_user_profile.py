import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from app.main import app
from app.core.config import settings
from app.db.session import SessionLocal
from app.database import User, UserRole, Project, ProjectMember, LoggedHour, GitContribution

def create_user_with_role(email: str, role: UserRole):
    """Helper to create a user with a specific role directly in DB."""
    db = SessionLocal()
    user = User(
        email=email,
        username=email,
        hashed_password="hashed_password", # dummy
        first_name="Test",
        last_name=role.value,
        display_name=f"Test {role.value}",
        role=role,
        is_verified=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return user

def login_user(client: TestClient, email: str):
    """Helper to bypass actual auth and get a token if possible, or use a mock."""
    # In this test environment, we'll try to use the login endpoint if it works with dummy password
    # Or we can use the same technique as test_permissions.py
    response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        json={"email": email, "password": "password123"} # Note: we need to set the password to "password123" in create_user
    )
    if response.status_code == 200:
        return response.json()["access_token"]
    return None

def create_and_login_user(client: TestClient, email: str, role: UserRole):
    """Helper to create a user with a specific role and return their access token."""
    from app.core.security import hash_password
    
    db = SessionLocal()
    # Check if exists
    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(
            email=email,
            username=email,
            hashed_password=hash_password("password123"),
            first_name="Test",
            last_name=role.value,
            display_name=f"Test {role.value}",
            role=role,
            is_verified=True,
            skills=["Python", "FastAPI"]
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    db.close()

    # Login
    response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        json={"email": email, "password": "password123"}
    )
    return response.json()["access_token"], user.id

def test_user_can_view_own_profile(client: TestClient):
    """Test that a user can view their own profile"""
    token, user_id = create_and_login_user(client, "user_own@example.com", UserRole.FRONTEND)
    
    response = client.get(
        f"{settings.API_V1_STR}/users/{user_id}/profile",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["email"] == "user_own@example.com"
    assert "skills" in data
    assert "contributions_summary" in data
    assert "activity_patterns" in data
    assert "projects_worked_on" in data
    assert "Python" in data["skills"]

def test_admin_can_view_any_profile(client: TestClient):
    """Test that admins can view any user's profile"""
    # 1. Create a regular user
    _, user_id = create_and_login_user(client, "regular_user@example.com", UserRole.FRONTEND)
    
    # 2. Login as admin
    admin_token, _ = create_and_login_user(client, "admin_user@example.com", UserRole.ADMIN)
    
    response = client.get(
        f"{settings.API_V1_STR}/users/{user_id}/profile",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert response.json()["id"] == user_id

def test_unauthorized_user_cannot_view_other_profile(client: TestClient):
    """Test that regular users cannot view others' profiles"""
    # 1. Create User A
    _, user_a_id = create_and_login_user(client, "user_a@example.com", UserRole.FRONTEND)
    
    # 2. Create User B and login
    user_b_token, _ = create_and_login_user(client, "user_b@example.com", UserRole.FRONTEND)
    
    # 3. User B tries to view User A's profile
    response = client.get(
        f"{settings.API_V1_STR}/users/{user_a_id}/profile",
        headers={"Authorization": f"Bearer {user_b_token}"}
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Not authorized to view this profile"

def test_nonexistent_user_returns_404(client: TestClient):
    """Test that requesting a non-existent user returns 404 (if admin)"""
    admin_token, _ = create_and_login_user(client, "admin_for_404@example.com", UserRole.ADMIN)
    
    response = client.get(
        f"{settings.API_V1_STR}/users/99999/profile",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_contributions_summary_aggregation(client: TestClient):
    """Test that the contributions summary correctly aggregates data"""
    # 1. Create user and login
    token, user_id = create_and_login_user(client, "agg_test@example.com", UserRole.BACKEND)
    
    # 2. Setup test data (Logged hours, projects, commits)
    db = SessionLocal()
    
    # Create a project
    project = Project(name="Aggregation Project", client_id=1) # Assume client 1 exists or create one
    db.add(project)
    db.commit()
    db.refresh(project)
    
    # Add user to project
    membership = ProjectMember(user_id=user_id, project_id=project.id, role="Lead")
    db.add(membership)
    
    # Log some hours
    log1 = LoggedHour(user_id=user_id, project_id=project.id, hours=5.5, date=datetime.now())
    log2 = LoggedHour(user_id=user_id, project_id=project.id, hours=10.0, date=datetime.now() - timedelta(days=1))
    db.add_all([log1, log2])
    
    # Add a commit
    commit = GitContribution(user_id=user_id, project_id=project.id, commit_hash="abc12345", provider="github")
    db.add(commit)
    
    db.commit()
    db.close()
    
    # 3. Get profile
    response = client.get(
        f"{settings.API_V1_STR}/users/{user_id}/profile",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    summary = data["contributions_summary"]
    assert summary["total_logged_hours"] == 15.5
    assert summary["total_commits"] == 1
    assert summary["projects_count"] == 1
    
    # Check activity patterns
    patterns = data["activity_patterns"]
    assert len(patterns["hours_by_week"]) > 0
    assert len(patterns["hours_by_month"]) > 0
    assert len(patterns["most_active_days"]) > 0
    
    # Check project details
    projects = data["projects_worked_on"]
    assert len(projects) == 1
    assert projects[0]["name"] == "Aggregation Project"
    assert projects[0]["hours_logged"] == 15.5
    assert projects[0]["role"] == "Lead"
