import os
import sys
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add the backend directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.db.base import Base
from app.dbmodels import Client, Project, Repository, User
from app.schemas.repository import RepositoryCreate
from app.services.repository import get_repositories_by_project, link_repository
from app.services.webhook import WebhookService

# Setup in-memory database
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def setup_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    # Create a test user
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password="hashed",
        display_name="Test User",
        first_name="Test",
        last_name="User",
    )
    db.add(user)
    db.commit()

    # Create a test client
    client = Client(name="Test Client", created_by=user.id)
    db.add(client)
    db.commit()

    # Create a test project
    project = Project(name="Test Project", client_id=client.id)
    db.add(project)
    db.commit()

    return db, project.id


def test_repo_mapping():
    db, project_id = setup_db()

    print(f"--- Verification for Project ID: {project_id} ---")

    # 1. Link a repository
    repo_data = RepositoryCreate(
        project_id=project_id,
        repository_url="https://github.com/test/repo",
        repository_name="test/repo",
        provider="github",
    )
    repo = link_repository(db, repo_data)
    print(f"Linked repository: {repo.repository_name} (ID: {repo.id})")

    # 2. List repositories
    repos = get_repositories_by_project(db, project_id)
    print(f"Repositories for project: {len(repos)}")
    assert len(repos) == 1

    # 3. Test WebhookService resolution
    print("\n--- Testing WebhookService resolution ---")

    test_urls = [
        "https://github.com/test/repo",
        "https://github.com/test/repo.git",
        "HTTPS://GITHUB.COM/TEST/REPO",
        "https://github.com/test/repo/",
    ]

    for url in test_urls:
        resolved_project = WebhookService._get_project_by_repository(db, url, "some name")
        if resolved_project and resolved_project.id == project_id:
            print(f"SUCCESS: Resolved {url} to Project {resolved_project.id}")
        else:
            print(f"FAILURE: Could not resolve {url}")
            sys.exit(1)

    # 4. Test missing repo
    missing_url = "https://github.com/other/repo"
    resolved_project = WebhookService._get_project_by_repository(db, missing_url, "other")
    if resolved_project is None:
        print(f"SUCCESS: Correctly returned None for unlinked repo: {missing_url}")
    else:
        print(f"FAILURE: Should not have resolved {missing_url}")
        sys.exit(1)

    print("\nVerification complete: ALL TESTS PASSED")


if __name__ == "__main__":
    test_repo_mapping()
