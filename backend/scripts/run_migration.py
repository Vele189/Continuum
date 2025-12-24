#!/usr/bin/env python3
"""
Standalone migration script for milestones.
Does not require app dependencies - uses sqlite3 directly.
"""
import sqlite3
import os

# Default database path (relative to backend directory)
DEFAULT_DB_PATH = "./continuum.db"

def get_db_path():
    """Get the database path from environment or use default."""
    db_path = os.getenv("DATABASE_URL", DEFAULT_DB_PATH)
    
    # Handle sqlite:/// prefix if present
    if db_path.startswith("sqlite:///"):
        db_path = db_path.replace("sqlite:///", "")
    
    # Handle relative paths
    if db_path.startswith("./"):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        backend_dir = os.path.dirname(script_dir)
        db_path = os.path.join(backend_dir, db_path[2:])
    elif not os.path.isabs(db_path):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        backend_dir = os.path.dirname(script_dir)
        db_path = os.path.join(backend_dir, db_path)
    
    return db_path

def migrate():
    """Run the migration."""
    db_path = get_db_path()
    
    print(f"Database path: {db_path}")
    
    if not os.path.exists(db_path):
        print(f"Warning: Database file does not exist at {db_path}")
        print("It will be created when the first table is created.")
    
    conn = sqlite3.connect(db_path)
    try:
        cur = conn.cursor()
        
        # Check if milestones table exists
        print("\n1. Checking if milestones table exists...")
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='milestones'")
        if cur.fetchone():
            print("   ✓ Milestones table already exists.")
        else:
            print("   Creating milestones table...")
            cur.execute("""
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
            """)
            print("   ✓ Milestones table created.")
        
        # Create index on milestones
        print("\n2. Creating index on milestones (project_id, status)...")
        cur.execute("""
            CREATE INDEX IF NOT EXISTS ix_milestones_project_id_status 
            ON milestones (project_id, status);
        """)
        print("   ✓ Index created.")
        
        # Check if milestone_id column exists in tasks
        print("\n3. Checking if milestone_id column exists in tasks...")
        cur.execute("PRAGMA table_info(tasks)")
        columns = [row[1] for row in cur.fetchall()]
        
        if "milestone_id" in columns:
            print("   ✓ milestone_id column already exists in tasks.")
        else:
            print("   Adding milestone_id column to tasks...")
            try:
                cur.execute("""
                    ALTER TABLE tasks 
                    ADD COLUMN milestone_id INTEGER 
                    REFERENCES milestones(id) ON DELETE SET NULL ON UPDATE CASCADE;
                """)
                print("   ✓ milestone_id column added.")
            except sqlite3.OperationalError as e:
                print(f"   ✗ Error adding column: {e}")
                print("   This might be because the tasks table doesn't exist yet.")
                raise
        
        # Create index on tasks.milestone_id
        print("\n4. Creating index on tasks (milestone_id)...")
        cur.execute("""
            CREATE INDEX IF NOT EXISTS ix_tasks_milestone_id 
            ON tasks (milestone_id);
        """)
        print("   ✓ Index created.")
        
        conn.commit()
        print("\n✅ Migration completed successfully!")
        
    except sqlite3.Error as e:
        conn.rollback()
        print(f"\n✗ Migration failed: {e}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()

