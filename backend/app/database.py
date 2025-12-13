# app/database.py
import sqlite3
from datetime import datetime

from app.utils.logger import get_logger


# Get a logger instance specifically for the database module
logger = get_logger(__name__) 

DATABASE_NAME = "continuum.db"

def init_db():
    """
    Initializes the SQLite database, connecting and creating all necessary tables
    if they do not already exist, and logging progress via the centralized logger.
    """
    logger.info("Starting database initialization process.")

    try:
        # Connect to the SQLite database file
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        # --- Table Creation (All SQL commands as defined) ---
        
        # 1. users Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                display_name TEXT NOT NULL,
                hourly_rate REAL DEFAULT 0.00,
                created_at TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now'))
            );
        """)
        logger.debug("Table 'users' verified/created.")


        # 2. clients Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT,
                created_by INTEGER,
                created_at TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now')),
                FOREIGN KEY (created_by) REFERENCES users (id)
            );
        """)
        logger.debug("Table 'clients' verified/created.")


        # 3. projects Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id INTEGER,
                name TEXT NOT NULL,
                description TEXT,
                status TEXT NOT NULL DEFAULT 'Active',
                created_at TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now')),
                FOREIGN KEY (client_id) REFERENCES clients (id)
            );
        """)
        logger.debug("Table 'projects' verified/created.")


        # 4. project_members Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS project_members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                role TEXT NOT NULL DEFAULT 'Member',
                added_at TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now')),
                FOREIGN KEY (project_id) REFERENCES projects (id),
                FOREIGN KEY (user_id) REFERENCES users (id),
                UNIQUE (project_id, user_id)
            );
        """)
        logger.debug("Table 'project_members' verified/created.")


        # 5. tasks Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                status TEXT NOT NULL DEFAULT 'To Do',
                assigned_to INTEGER,
                created_at TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now')),
                updated_at TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now')),
                FOREIGN KEY (project_id) REFERENCES projects (id),
                FOREIGN KEY (assigned_to) REFERENCES users (id)
            );
        """)
        logger.debug("Table 'tasks' verified/created.")


        # 6. logged_hours Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS logged_hours (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                task_id INTEGER,
                project_id INTEGER NOT NULL,
                hours REAL NOT NULL,
                note TEXT,
                logged_at TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now')),
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (task_id) REFERENCES tasks (id),
                FOREIGN KEY (project_id) REFERENCES projects (id)
            );
        """)
        logger.debug("Table 'logged_hours' verified/created.")


        # 7. git_contributions Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS git_contributions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                project_id INTEGER NOT NULL,
                commit_hash TEXT NOT NULL UNIQUE,
                commit_message TEXT,
                branch TEXT,
                committed_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (project_id) REFERENCES projects (id)
            );
        """)
        logger.debug("Table 'git_contributions' verified/created.")


        # 8. system_logs Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS system_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                level TEXT NOT NULL,
                message TEXT NOT NULL,
                meta TEXT,
                created_at TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now'))
            );
        """)
        logger.debug("Table 'system_logs' verified/created.")

        # Commit changes and close connection
        conn.commit()
        conn.close()
        
        logger.info("Database initialized successfully: all 8 tables created or verified.")

    except sqlite3.Error as e:
        logger.error(f"FATAL DB ERROR: Could not complete schema creation: {e}", exc_info=True)
        # Re-raise the exception so the main application startup can handle the failure
        raise