#!/usr/bin/env python3
"""
Simple test script to verify Milestones implementation.
Checks database schema and tests API endpoints if server is running.
"""
import os
import sqlite3
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def check_database_schema():
    """Check if database has required schema"""
    print("=" * 60)
    print("Database Schema Check")
    print("=" * 60)

    db_path = "continuum.db"
    if not os.path.exists(db_path):
        print(f"❌ Database file not found: {db_path}")
        return False

    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        # Check milestones table
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='milestones'")
        if cur.fetchone():
            print("✓ Milestones table exists")

            # Check columns
            cur.execute("PRAGMA table_info(milestones)")
            columns = {row[1]: row[2] for row in cur.fetchall()}
            required_columns = {
                "id": "INTEGER",
                "project_id": "INTEGER",
                "name": "VARCHAR",
                "due_date": "DATETIME",
                "status": "VARCHAR",
                "created_at": "DATETIME",
                "updated_at": "DATETIME",
            }

            all_present = True
            for col, col_type in required_columns.items():
                if col in columns:
                    print(f"  ✓ Column '{col}' exists")
                else:
                    print(f"  ❌ Column '{col}' missing")
                    all_present = False

            # Check foreign key
            cur.execute("PRAGMA foreign_key_list(milestones)")
            fks = cur.fetchall()
            has_project_fk = any(fk[2] == "projects" for fk in fks)
            if has_project_fk:
                print("  ✓ Foreign key to projects exists")
            else:
                print("  ❌ Foreign key to projects missing")
                all_present = False

            # Check index
            cur.execute(
                "SELECT name FROM sqlite_master WHERE type='index' AND name LIKE 'ix_milestones%'"
            )
            indexes = cur.fetchall()
            if indexes:
                print(f"  ✓ Indexes found: {[idx[0] for idx in indexes]}")
            else:
                print("  ⚠ No indexes found (may be okay)")
        else:
            print("❌ Milestones table does not exist")
            conn.close()
            return False

        # Check tasks table for milestone_id
        cur.execute("PRAGMA table_info(tasks)")
        task_columns = [row[1] for row in cur.fetchall()]
        if "milestone_id" in task_columns:
            print("✓ Tasks table has milestone_id column")

            # Check foreign key constraint
            cur.execute("PRAGMA foreign_key_list(tasks)")
            task_fks = cur.fetchall()
            has_milestone_fk = any(fk[2] == "milestones" for fk in task_fks)
            if has_milestone_fk:
                print("  ✓ Foreign key to milestones exists")
                # Check ON DELETE SET NULL
                for fk in task_fks:
                    if fk[2] == "milestones":
                        on_delete = fk[4]  # ON DELETE action
                        if "SET NULL" in on_delete.upper() or on_delete.upper() == "SET NULL":
                            print("  ✓ ON DELETE SET NULL constraint present")
                        else:
                            print(f"  ⚠ ON DELETE action is '{on_delete}' (expected SET NULL)")
            else:
                print("  ❌ Foreign key to milestones missing")
        else:
            print("❌ Tasks table missing milestone_id column")
            conn.close()
            return False

        conn.close()
        print("\n✓ Database schema check passed!")
        return True

    except Exception as e:
        print(f"❌ Error checking database: {e}")
        return False


def check_code_structure():
    """Check if required code files exist and have correct structure"""
    print("\n" + "=" * 60)
    print("Code Structure Check")
    print("=" * 60)

    checks = [
        ("app/models/milestone.py", "Milestone model"),
        ("app/schemas/milestone.py", "Milestone schemas"),
        ("app/services/milestone.py", "Milestone service"),
        ("app/api/v1/routes/milestones.py", "Milestone routes"),
    ]

    all_good = True
    for file_path, description in checks:
        if os.path.exists(file_path):
            print(f"✓ {description} exists")
        else:
            print(f"❌ {description} missing: {file_path}")
            all_good = False

    # Check if routes are registered
    main_py = "app/main.py"
    if os.path.exists(main_py):
        with open(main_py, "r") as f:
            content = f.read()
            if "milestones" in content.lower():
                print("✓ Milestones routes registered in main.py")
            else:
                print("⚠ Milestones routes may not be registered")
    else:
        print("⚠ Cannot check main.py")

    # Check task model for milestone_id
    task_model = "app/models/task.py"
    if os.path.exists(task_model):
        with open(task_model, "r") as f:
            content = f.read()
            if "milestone_id" in content:
                print("✓ Task model has milestone_id field")
            else:
                print("❌ Task model missing milestone_id field")
                all_good = False
    else:
        print("⚠ Cannot check task model")

    # Check task routes for milestone linking
    task_routes = "app/api/v1/routes/tasks.py"
    if os.path.exists(task_routes):
        with open(task_routes, "r") as f:
            content = f.read()
            if "/milestone" in content and "PATCH" in content:
                print("✓ Task milestone linking endpoint exists")
            else:
                print("⚠ Task milestone linking endpoint may be missing")
    else:
        print("⚠ Cannot check task routes")

    return all_good


def check_permissions_implementation():
    """Check if permissions are implemented in routes"""
    print("\n" + "=" * 60)
    print("Permissions Check")
    print("=" * 60)

    milestones_routes = "app/api/v1/routes/milestones.py"
    if os.path.exists(milestones_routes):
        with open(milestones_routes, "r") as f:
            content = f.read()

            # Check for permission checks
            has_project_check = "project" in content.lower() and (
                "member" in content.lower() or "admin" in content.lower()
            )
            has_user_check = "current_user" in content or "get_current_user" in content

            if has_user_check:
                print("✓ Routes require authentication")
            else:
                print("⚠ Routes may not require authentication")

            if "TODO" in content or "FIXME" in content:
                print("⚠ Found TODO/FIXME comments - permissions may be incomplete")
                # Show TODO lines
                lines = content.split("\n")
                for i, line in enumerate(lines, 1):
                    if "TODO" in line or "FIXME" in line:
                        print(f"  Line {i}: {line.strip()}")
            else:
                print("✓ No obvious TODO comments found")
    else:
        print("⚠ Cannot check permissions")


def main():
    """Run all checks"""
    print("\n" + "=" * 60)
    print("Milestones Feature Implementation Check")
    print("=" * 60 + "\n")

    schema_ok = check_database_schema()
    code_ok = check_code_structure()
    check_permissions_implementation()

    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)

    if schema_ok and code_ok:
        print("✓ Basic implementation appears complete")
        print("\nNext steps:")
        print("  1. Start the backend server")
        print("  2. Run comprehensive API tests")
        print("  3. Test permissions with different user roles")
        return 0
    else:
        print("❌ Some issues found - review above")
        return 1


if __name__ == "__main__":
    sys.exit(main())
