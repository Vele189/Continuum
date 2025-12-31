import os
import sqlite3
import sys

# Add backend directory to path so we can import app config if needed
sys.path.append(os.path.join(os.getcwd(), ".."))

from app.core.config import settings  # pylint: disable=wrong-import-position


def migrate():
    # Force absolute path for SQLite to avoid CWD issues
    db_url = settings.DATABASE_URL
    if db_url.startswith("sqlite:///"):
        # Strip sqlite:/// prefix
        db_path = db_url.replace("sqlite:///", "")

        # If it was relative (./), resolve it
        if db_path.startswith("./"):
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            db_path = os.path.join(base_dir, db_path[2:])

        print(f"Resolved Database Path: {db_path}")
    else:
        print("Not a SQLite database, skipping specific migration logic.")
        return

    print(f"Connecting to database: {db_path}")
    conn = sqlite3.connect(db_path)
    try:
        cur = conn.cursor()

        print("Checking if milestones table exists...")
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='milestones'")
        if cur.fetchone():
            print("Milestones table already exists.")
        else:
            print("Creating milestones table...")
            cur.execute(
                """
                CREATE TABLE milestones (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id INTEGER NOT NULL,
                    name VARCHAR NOT NULL,
                    due_date DATETIME,
                    status VARCHAR DEFAULT 'not_started',
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE ON UPDATE CASCADE
                );
            """
            )
            print("Milestones table created.")

            print("Creating index on milestones (project_id, status)...")
            cur.execute(
                "CREATE INDEX ix_milestones_project_id_status ON milestones (project_id, status);"
            )
            print("Index created.")

        print("Checking if milestone_id column exists in tasks...")
        cur.execute("PRAGMA table_info(tasks)")
        columns = [row[1] for row in cur.fetchall()]

        if "milestone_id" in columns:
            print("milestone_id column already exists in tasks.")
        else:
            print("Adding milestone_id column to tasks...")
            cur.execute(
                "ALTER TABLE tasks ADD COLUMN milestone_id INTEGER REFERENCES milestones(id) ON DELETE SET NULL ON UPDATE CASCADE;"
            )
            print("milestone_id column added.")

            print("Creating index on tasks (milestone_id)...")
            cur.execute("CREATE INDEX ix_tasks_milestone_id ON tasks (milestone_id);")
            print("Index created.")

        conn.commit()
        print("Migration complete.")
    finally:
        conn.close()


if __name__ == "__main__":
    migrate()
