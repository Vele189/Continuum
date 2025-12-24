from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.core.config import settings
from app.db.session import SessionLocal
from app.dbmodels import User

def test_password_reset_flow(client: TestClient):
    # 1. Register User
    email = "reset_test@example.com"
    old_password = "oldpassword123"
    client.post(
        f"{settings.API_V1_STR}/users/",
        json={
            "email": email, 
            "password": old_password,
            "first_name": "Reset",
            "last_name": "Test"
        },
    )
    
    # 2. Request Password Reset
    response = client.post(f"{settings.API_V1_STR}/auth/password-recovery/{email}")
    assert response.status_code == 200
    
    # 3. Get Token from DB (Mocking email receipt)
    db = SessionLocal()
    user = db.query(User).filter(User.email == email).first()
    reset_token = user.password_reset_token
    assert reset_token is not None
    db.close()
    
    # 4. Success Reset
    new_password = "newpassword456"
    response = client.post(
        f"{settings.API_V1_STR}/auth/reset-password",
        json={"token": reset_token, "new_password": new_password}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Password updated successfully"
    
    # 5. Verify Login with New Password
    login_response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        json={"email": email, "password": new_password}
    )
    assert login_response.status_code == 200
    
    # 6. Verify Old Password Fails
    fail_response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        json={"email": email, "password": old_password}
    )
    assert fail_response.status_code == 401  # Unauthorized
