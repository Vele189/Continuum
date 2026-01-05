#!/usr/bin/env python3
"""Add updated_at column to clients table if it doesn't exist"""
from app.database import engine
from sqlalchemy import inspect, text


def add_updated_at_column():
    """Add updated_at column to clients table"""
    inspector = inspect(engine)
    columns = [col["name"] for col in inspector.get_columns("clients")]

    if "updated_at" in columns:
        print("Column 'updated_at' already exists in clients table")
        return

    with engine.connect() as conn:
        # We'll add the column and then set a default value
        conn.execute(
            text(
                """
            ALTER TABLE clients
            ADD COLUMN updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        """
            )
        )
        conn.commit()
        print("Successfully added 'updated_at' column to clients table")


if __name__ == "__main__":
    add_updated_at_column()
