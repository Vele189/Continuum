"""
Migration script to add skills column to users table.
Run this script to add the skills JSON column to existing database.
"""

import sqlite3
import os

# Database path
DB_PATH = os.path.join(os.path.dirname(__file__), "continuum.db")

def upgrade():
    """Add skills column to users table"""
    print("Starting migration: Adding skills column to users table...")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Check if column already exists
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'skills' in columns:
            print(" Skills column already exists. Skipping migration.")
            return
        
        # Add skills column
        cursor.execute("""
            ALTER TABLE users 
            ADD COLUMN skills TEXT
        """)
        
        conn.commit()
        print(" Successfully added skills column to users table.")
        
    except sqlite3.Error as e:
        print(f" Error during migration: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

def downgrade():
    """Remove skills column from users table"""
    print("Starting rollback: Removing skills column from users table...")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # SQLite doesn't support DROP COLUMN directly
        # We need to recreate the table without the skills column
        
        # Get current table schema
        cursor.execute("PRAGMA table_info(users)")
        columns = cursor.fetchall()
        
        # Filter out skills column
        columns_without_skills = [col for col in columns if col[1] != 'skills']
        
        # Create column definitions
        column_defs = []
        for col in columns_without_skills:
            col_def = f"{col[1]} {col[2]}"
            if col[3]:  # NOT NULL
                col_def += " NOT NULL"
            if col[4] is not None:  # DEFAULT
                col_def += f" DEFAULT {col[4]}"
            if col[5]:  # PRIMARY KEY
                col_def += " PRIMARY KEY"
            column_defs.append(col_def)
        
        # Create new table
        cursor.execute(f"""
            CREATE TABLE users_new (
                {', '.join(column_defs)}
            )
        """)
        
        # Copy data
        column_names = [col[1] for col in columns_without_skills]
        cursor.execute(f"""
            INSERT INTO users_new ({', '.join(column_names)})
            SELECT {', '.join(column_names)}
            FROM users
        """)
        
        # Drop old table and rename new one
        cursor.execute("DROP TABLE users")
        cursor.execute("ALTER TABLE users_new RENAME TO users")
        
        conn.commit()
        print(" Successfully removed skills column from users table.")
        
    except sqlite3.Error as e:
        print(f" Error during rollback: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "downgrade":
        downgrade()
    else:
        upgrade()
