from app.core.config import settings
from app.db.session import SessionLocal
from app.dbmodels import User, UserRole
from fastapi.testclient import TestClient


def create_and_login_user(client: TestClient, email: str, role: UserRole):
    """Helper to create a user with a specific role and return their access token."""
    user_data = {
        "email": email,
        "password": "password123",
        "first_name": "Test",
        "last_name": role.value,
    }

    # Use API to create (gets default role)
    client.post(f"{settings.API_V1_STR}/users/", json=user_data)

    # Update role in DB
    db = SessionLocal()
    user = db.query(User).filter(User.email == email).first()
    user.role = role
    db.add(user)
    db.commit()
    db.close()

    # Login
    response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        json={"email": email, "password": user_data["password"]},
    )
    return response.json()["access_token"]


def test_admin_access_dashboard(client: TestClient):
    """Test that ADMIN role can access admin dashboard."""
    token = create_and_login_user(client, "admin@example.com", UserRole.ADMIN)

    response = client.get(
        f"{settings.API_V1_STR}/admin/dashboard", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert "Welcome Admin" in response.json()["message"]


def test_project_manager_access_dashboard(client: TestClient):
    """Test that PROJECTMANAGER role can access admin dashboard."""
    token = create_and_login_user(client, "pm@example.com", UserRole.PROJECTMANAGER)

    response = client.get(
        f"{settings.API_V1_STR}/admin/dashboard", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert "Welcome Admin" in response.json()["message"]


def test_members_access_denied(client: TestClient):
    """Test that non-admin roles cannot access admin dashboard."""
    roles_to_test = [
        UserRole.FRONTEND,
        UserRole.BACKEND,
        UserRole.DESIGNER,
        UserRole.CLIENT,  # CLIENT is not an admin role
    ]

    for role in roles_to_test:
        email = f"{role.value}@example.com"
        token = create_and_login_user(client, email, role)

        response = client.get(
            f"{settings.API_V1_STR}/admin/dashboard", headers={"Authorization": f"Bearer {token}"}
        )
        assert (
            response.status_code == 403
        ), f"Expected 403 for role {role.value}, got {response.status_code}"
        assert response.json()["detail"] == "The user doesn't have enough privileges"
