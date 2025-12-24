from fastapi.testclient import TestClient
from app.core.config import settings
from app.db.session import SessionLocal
from app.dbmodels import User


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

    assert response.status_code == 201  # Created
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
    assert response.status_code == 401  # Unauthorized


def test_duplicate_user(client: TestClient):
    payload = {
        "email": "test4@example.com",
        "password": "password123",
        "first_name": "Test",
        "last_name": "User"
    }
    response = client.post(f"{settings.API_V1_STR}/users/", json=payload)
    assert response.status_code == 201  # Created

    response = client.post(f"{settings.API_V1_STR}/users/", json=payload)
    assert response.status_code == 409  # Conflict


def test_refresh_token(client: TestClient):
    # 1. Login to get tokens
    client.post(
        f"{settings.API_V1_STR}/users/",
        json={
            "email": "refresh_test@example.com",
            "password": "password123",
            "first_name": "Test",
            "last_name": "User"
        },
    )
    login_response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        json={"email": "refresh_test@example.com", "password": "password123"},
    )
    tokens = login_response.json()
    refresh_token = tokens["refresh_token"]

    # 2. Use refresh token to get new access token
    refresh_response = client.post(
        f"{settings.API_V1_STR}/auth/refresh-token",
        params={"refresh_token": refresh_token}
    )
    assert refresh_response.status_code == 200
    new_tokens = refresh_response.json()
    assert "access_token" in new_tokens
    assert "refresh_token" in new_tokens


def test_verify_email(client: TestClient):
    # Register
    email = "verify_test@example.com"
    client.post(
        f"{settings.API_V1_STR}/users/",
        json={
            "email": email,
            "password": "password123",
            "first_name": "Test",
            "last_name": "User"
        },
    )

    # Get token from DB directly (simulating clicking link)
    db = SessionLocal()
    user = db.query(User).filter(User.email == email).first()
    token = user.verification_token
    assert token is not None
    assert user.is_verified is False
    db.close()

    # Verify
    response = client.get(f"{settings.API_V1_STR}/users/verify-email", params={"token": token})
    assert response.status_code == 200
    assert response.json()["message"] == "Email verified successfully"

    # Check DB again
    db = SessionLocal()
    user = db.query(User).filter(User.email == email).first()
    assert user.is_verified is True
    assert user.verification_token is None
    db.close()
