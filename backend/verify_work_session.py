import os

from app.database import SessionLocal
from app.dbmodels import (
    Base,
    LoggedHour,
    Project,
    ProjectMember,
    User,
    WorkSession,
    WorkSessionStatus,
)
from app.schemas.work_session import WorkSessionCreate
from app.services import work_session as service
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def test_lifecycle():
    db = SessionLocal()
    try:
        # 1. Setup mock user and project
        user = db.query(User).first()
        if not user:
            print("No user found in DB, creating one...")
            user = User(
                username="testuser",
                email="test@example.com",
                hashed_password="pw",
                first_name="Test",
                last_name="User",
                display_name="Test User",
            )
            db.add(user)
            db.commit()
            db.refresh(user)

        project = db.query(Project).first()
        if not project:
            print("No project found in DB, creating one...")
            from app.dbmodels import Client

            client = db.query(Client).first()
            if not client:
                client = Client(name="Test Client")
                db.add(client)
                db.commit()
                db.refresh(client)
            project = Project(name="Test Project", client_id=client.id)
            db.add(project)
            db.commit()
            db.refresh(project)

        # Cleanup existing sessions
        db.query(WorkSession).filter(WorkSession.user_id == user.id).delete()
        db.commit()

        print("Testing Start Session...")
        create_data = WorkSessionCreate(project_id=project.id, note="Testing session")
        ws = service.start_session(db, user, create_data)
        print(f"Started session ID: {ws.id}, Status: {ws.status}")

        print("Testing Start session while one exists (Expecting 400)...")
        try:
            service.start_session(db, user, create_data)
        except Exception as e:
            print(f"Caught expected error: {e.detail}")

        print("Testing Pause Session...")
        ws = service.pause_session(db, ws.id, user)
        print(f"Paused session. Status: {ws.status}, Duration: {ws.duration_seconds}s")

        print("Testing Resume Session...")
        ws = service.resume_session(db, ws.id, user)
        print(f"Resumed session. Status: {ws.status}")

        print("Testing Stop Session...")
        ws = service.stop_session(db, ws.id, user)
        print(f"Stopped session. Status: {ws.status}, Total Duration: {ws.duration_seconds}s")

        # Verify LoggedHour
        lh = (
            db.query(LoggedHour)
            .filter(LoggedHour.user_id == user.id)
            .order_by(LoggedHour.logged_at.desc())
            .first()
        )
        if lh:
            print(f"LoggedHour created: {lh.hours}h, Note: {lh.note}")
        else:
            print("FAILED: LoggedHour not found!")

    finally:
        db.close()


if __name__ == "__main__":
    os.environ["DATABASE_URL"] = "sqlite:///continuum.db"
    test_lifecycle()
