from fastapi.testclient import TestClient
from app.core.config import settings

def test_register_user(client: TestClient):
    response = client.post(
        f"{settings.API_V1_STR}/users/",
        json={
            "email": "test@example.com", 
            "password": "password123",
            "first_name": "Test",
            "last_name": "User"
        },
    )
    # 200 is used in the implementation, though 201 is more standard for creation. 
    # Current implementation returns the created user object which defaults to 200 OK in FastAPI unless specified otherwise.
    assert response.status_code == 200 
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["first_name"] == "Test"
    assert data["last_name"] == "User"
    assert "id" in data
    assert "hashed_password" not in data
    # Role default
    assert data["role"] == "frontend"

def test_login_user(client: TestClient):
    # First create user
    client.post(
        f"{settings.API_V1_STR}/users/",
        json={
            "email": "test2@example.com", 
            "password": "password123",
            "first_name": "Test",
            "last_name": "User"
        },
    )
    
    # Login
    response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        json={"email": "test2@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password(client: TestClient):
    client.post(
        f"{settings.API_V1_STR}/users/",
        json={
            "email": "test3@example.com", 
            "password": "password123",
            "first_name": "Test",
            "last_name": "User"
        },
    )
    response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        json={"email": "test3@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 400

def test_duplicate_user(client: TestClient):
    payload = {
        "email": "test4@example.com", 
        "password": "password123",
        "first_name": "Test",
        "last_name": "User"
    }
    response = client.post(f"{settings.API_V1_STR}/users/", json=payload)
    assert response.status_code == 200
    
    response = client.post(f"{settings.API_V1_STR}/users/", json=payload)
    assert response.status_code == 400
