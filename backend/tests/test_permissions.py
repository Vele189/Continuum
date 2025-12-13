from fastapi.testclient import TestClient
from app.core.config import settings
from app.db.session import SessionLocal
from app.models.user import User, UserRole

def create_and_login_user(client: TestClient, email: str, role: UserRole):
    # Register/Create user manually to set role
    user_data = {
        "email": email, 
        "password": "password123",
        "first_name": "Test",
        "last_name": role.value
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
        json={"email": email, "password": user_data["password"]}
    )
    return response.json()["access_token"]

def test_admin_access_dashboard(client: TestClient):
    token = create_and_login_user(client, "admin@example.com", UserRole.CLIENT)
    
    response = client.get(
        f"{settings.API_V1_STR}/admin/dashboard",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert "Welcome Admin" in response.json()["message"]

def test_members_access_denied(client: TestClient):
    roles_to_test = [
        UserRole.FRONTEND,
        UserRole.BACKEND,
        UserRole.DESIGNER,
        UserRole.PROJECTMANAGER
    ]
    
    for role in roles_to_test:
        email = f"{role.value}@example.com"
        token = create_and_login_user(client, email, role)
        
        response = client.get(
            f"{settings.API_V1_STR}/admin/dashboard",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 403
        assert response.json()["detail"] == "The user doesn't have enough privileges"
