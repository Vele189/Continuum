import sqlite3
import os

db_path = "continuum.db"
if not os.path.exists(db_path):
    print(f"Error: {db_path} does not exist.")
else:
    print(f"Opening {db_path}...")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # Check Milestones
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='milestones'")
    row = cur.fetchone()
    if row:
        print("Milestones table found.")
    else:
        print("Milestones table NOT found.")

    # Check Task columns
    cur.execute("PRAGMA table_info(tasks)")
    columns = [row[1] for row in cur.fetchall()]
    if "milestone_id" in columns:
        print("milestone_id column found in tasks.")
    else:
        print(f"milestone_id column NOT found in tasks. Columns: {columns}")
    
    conn.close()
