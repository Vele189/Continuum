#!/usr/bin/env python3
"""Migrate git_contributions table to add new columns and update constraints"""
import sys

from app.database import engine
from sqlalchemy import inspect, text
from sqlalchemy.exc import OperationalError


def migrate_git_contributions():
    """Migrate git_contributions table to add new columns and update constraints"""
    inspector = inspect(engine)

    # Check if table exists
    if "git_contributions" not in inspector.get_table_names():
        print("Table 'git_contributions' does not exist. It will be created on next app start.")
        return

    columns = {col["name"]: col for col in inspector.get_columns("git_contributions")}

    with engine.connect() as conn:
        # Start a transaction
        trans = conn.begin()

        try:
            # 1. Add task_id column if it doesn't exist
            if "task_id" not in columns:
                print("Adding 'task_id' column...")
                conn.execute(
                    text(
                        """
                    ALTER TABLE git_contributions
                    ADD COLUMN task_id INTEGER REFERENCES tasks(id) ON DELETE SET NULL ON UPDATE CASCADE
                """
                    )
                )
                print("✓ Added 'task_id' column")
            else:
                print("Column 'task_id' already exists")

            # 2. Add provider column if it doesn't exist
            if "provider" not in columns:
                print("Adding 'provider' column...")
                # SQLite: Add column as nullable first, then update, then we can't make it NOT NULL without recreating table
                # For now, we'll add it as nullable and handle NOT NULL at application level
                conn.execute(
                    text(
                        """
                    ALTER TABLE git_contributions
                    ADD COLUMN provider TEXT DEFAULT 'github'
                """
                    )
                )
                # Update existing rows to have a provider
                conn.execute(
                    text(
                        """
                    UPDATE git_contributions
                    SET provider = 'github'
                    WHERE provider IS NULL
                """
                    )
                )
                print("✓ Added 'provider' column (nullable, default 'github')")
            else:
                print("Column 'provider' already exists")

            # 3. Add commit_url column if it doesn't exist
            if "commit_url" not in columns:
                print("Adding 'commit_url' column...")
                conn.execute(
                    text(
                        """
                    ALTER TABLE git_contributions
                    ADD COLUMN commit_url TEXT
                """
                    )
                )
                print("✓ Added 'commit_url' column")
            else:
                print("Column 'commit_url' already exists")

            # 4. Handle committed_at -> created_at
            if "committed_at" in columns and "created_at" not in columns:
                print("Renaming 'committed_at' to 'created_at'...")
                # SQLite doesn't support RENAME COLUMN directly in older versions
                # We'll add created_at and copy data, then drop committed_at
                conn.execute(
                    text(
                        """
                    ALTER TABLE git_contributions
                    ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                """
                    )
                )
                conn.execute(
                    text(
                        """
                    UPDATE git_contributions
                    SET created_at = committed_at
                    WHERE committed_at IS NOT NULL
                """
                    )
                )
                # Note: We can't easily drop committed_at in SQLite without recreating the table
                # For now, we'll leave it and the model will use created_at
                print("✓ Added 'created_at' column and copied data from 'committed_at'")
            elif "created_at" not in columns:
                print("Adding 'created_at' column...")
                conn.execute(
                    text(
                        """
                    ALTER TABLE git_contributions
                    ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                """
                    )
                )
                print("✓ Added 'created_at' column")
            else:
                print("Column 'created_at' already exists")

            # 4b. Handle committed_at constraint - set default for new inserts
            # Since SQLite doesn't support ALTER COLUMN, we'll ensure committed_at has a default
            # by updating existing NULL values and the service will set it on new inserts
            if "committed_at" in columns:
                print("Updating 'committed_at' for existing rows...")
                conn.execute(
                    text(
                        """
                    UPDATE git_contributions
                    SET committed_at = COALESCE(committed_at, created_at, CURRENT_TIMESTAMP)
                    WHERE committed_at IS NULL
                """
                    )
                )
                print("✓ Updated 'committed_at' for existing rows")

            # 5. Create composite unique index
            # SQLite doesn't support DROP CONSTRAINT easily, so we'll create the composite unique index
            # The old unique constraint on commit_hash alone will remain but won't be enforced by the model
            try:
                # Check if index already exists
                indexes = inspector.get_indexes("git_contributions")
                has_composite_index = any(
                    idx.get("name") == "uix_project_commit" for idx in indexes
                )

                if not has_composite_index:
                    conn.execute(
                        text(
                            """
                        CREATE UNIQUE INDEX uix_project_commit
                        ON git_contributions(project_id, commit_hash)
                    """
                        )
                    )
                    print("✓ Created composite unique index on (project_id, commit_hash)")
                else:
                    print("Composite unique index 'uix_project_commit' already exists")
            except OperationalError as e:
                if "already exists" not in str(e).lower() and "duplicate" not in str(e).lower():
                    print(f"Note: Could not create index (may already exist): {e}")
                else:
                    print("✓ Composite unique index already exists")

            # Commit the transaction
            trans.commit()
            print("\n✓ Migration completed successfully!")

        except Exception as e:
            trans.rollback()
            print(f"\n✗ Migration failed: {e}")
            raise


if __name__ == "__main__":
    try:
        migrate_git_contributions()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
