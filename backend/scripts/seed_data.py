import os
import sys

# Add the backend directory to sys.path to allow imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.security import hash_password
from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.dbmodels import Client, Project, ProjectMember, Repository, User, UserRole


def seed_data():
    db = SessionLocal()
    try:
        # 1. Create Admin User
        admin_email = "admin@continuum.ai"
        admin = db.query(User).filter(User.email == admin_email).first()
        if not admin:
            print(f"Creating admin user: {admin_email}")
            admin = User(
                email=admin_email,
                hashed_password=hash_password("admin123"),
                first_name="Admin",
                last_name="User",
                display_name="Admin",
                username="admin",
                role=UserRole.ADMIN,
                is_verified=True,
            )
            db.add(admin)
            db.commit()
            db.refresh(admin)
        else:
            print(f"Admin user already exists: {admin_email}")

        # 2. Create Demo Client
        client_name = "Demo Client"
        client = db.query(Client).filter(Client.name == client_name).first()
        if not client:
            print(f"Creating client: {client_name}")
            client = Client(name=client_name, email="demo@client.com", created_by=admin.id)
            db.add(client)
            db.commit()
            db.refresh(client)
        else:
            print(f"Client already exists: {client_name}")

        # 3. Create Project
        project_name = "Continuum Platform"
        project = db.query(Project).filter(Project.name == project_name).first()
        if not project:
            print(f"Creating project: {project_name}")
            project = Project(
                name=project_name,
                description="The ultimate project intelligence platform.",
                client_id=client.id,
                status="active",
            )
            db.add(project)
            db.commit()
            db.refresh(project)

            # Add Admin as Project Member
            member = ProjectMember(project_id=project.id, user_id=admin.id, role="owner")
            db.add(member)
            db.commit()
        else:
            print(f"Project already exists: {project_name}")

        # 4. Create Repository
        repo_url = "https://github.com/continuum/frontend"
        repo = db.query(Repository).filter(Repository.repository_url == repo_url).first()
        if not repo:
            print(f"Creating repository: {repo_url}")
            repo = Repository(
                project_id=project.id,
                repository_url=repo_url,
                repository_name="continuum-frontend",
                provider="github",
                is_active=True,
            )
            db.add(repo)
            db.commit()
        else:
            print(f"Repository already exists: {repo_url}")

        print("Seeding completed successfully!")

    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
