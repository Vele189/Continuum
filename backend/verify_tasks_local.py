import logging
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

os.environ["ENV"] = "test"

from app.main import app
from app.db.base import Base
from app.api import deps
from app.models.user import User, UserRole
from app.models.project import Project
from app.core.security import create_access_token

# Setup Test DB
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_continuum.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[deps.get_db] = override_get_db

client = TestClient(app)

def setup_data():
    db = TestingSessionLocal()
    # Create Admin User (Project Manager)
    admin_user = User(
        email="admin@test.com", 
        hashed_password="hashed_pw", 
        first_name="Admin", 
        last_name="User",
        role=UserRole.PROJECTMANAGER,
        is_verified=True
    )
    # Create Regular User (Member)
    regular_user = User(
        email="user@test.com", 
        hashed_password="hashed_pw", 
        first_name="Regular", 
        last_name="User",
        role=UserRole.FRONTEND,
        is_verified=True
    )
    db.add(admin_user)
    db.add(regular_user)
    db.commit()
    
    # Create Project
    project = Project(
        name="Test Project",
        description="A project for testing tasks",
        client_id=1,
        status="Active"
    )
    db.add(project)
    db.commit()
    
    admin_id = admin_user.id
    user_id = regular_user.id
    project_id = project.id
    db.close()
    
    # Generate Tokens
    admin_token = create_access_token(subject=admin_id)
    user_token = create_access_token(subject=user_id)
    
    return admin_token, user_token, project_id, user_id

def verify_tasks():
    print("Setting up test data...")
    admin_token, user_token, project_id, user_id = setup_data()
    
    admin_auth = {"Authorization": f"Bearer {admin_token}"}
    user_auth = {"Authorization": f"Bearer {user_token}"}
    
    print("\n--- Testing Task Creation ---")
    response = client.post(
        "/api/v1/tasks/",
        json={"title": "New Task", "description": "Test description", "project_id": project_id},
        headers=user_auth
    )
    print(f"Create Task Response: {response.status_code}")
    if response.status_code != 200:
        print(response.json())
        exit(1)
    task_id = response.json()["id"]
    print(f"Task Created with ID: {task_id}")

    print("\n--- Testing List Tasks ---")
    response = client.get(
        f"/api/v1/tasks/?project_id={project_id}",
        headers=user_auth
    )
    print(f"List Tasks Response: {response.status_code}")
    print(f"Tasks Found: {len(response.json())}")
    assert len(response.json()) >= 1

    print("\n--- Testing Update Task ---")
    response = client.put(
        f"/api/v1/tasks/{task_id}",
        json={"status": "In Progress"},
        headers=user_auth
    )
    print(f"Update Task Response: {response.status_code}")
    assert response.json()["status"] == "In Progress"

    print("\n--- Testing Assign Task ---")
    response = client.post(
        f"/api/v1/tasks/{task_id}/assign?user_id={user_id}",
        headers=user_auth
    )
    print(f"Assign Task Response: {response.status_code}")
    assert response.json()["assigned_to"] == user_id

    print("\n--- Testing Delete Task (As Regular User - Should Fail) ---")
    response = client.delete(
        f"/api/v1/tasks/{task_id}",
        headers=user_auth
    )
    print(f"Delete (User) Response: {response.status_code}")
    assert response.status_code == 403

    print("\n--- Testing Delete Task (As Admin - Should Succeed) ---")
    response = client.delete(
        f"/api/v1/tasks/{task_id}",
        headers=admin_auth
    )
    print(f"Delete (Admin) Response: {response.status_code}")
    assert response.status_code == 200

    print("\n--- Verification Completed Successfully ---")

if __name__ == "__main__":
    # Clean up old test db
    if os.path.exists("test_continuum.db"):
        os.remove("test_continuum.db")
    
    try:
        verify_tasks()
    finally:
        if os.path.exists("test_continuum.db"):
            os.remove("test_continuum.db")
