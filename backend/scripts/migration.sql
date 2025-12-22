CREATE TABLE IF NOT EXISTS milestones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    name VARCHAR NOT NULL,
    due_date DATETIME,
    status VARCHAR DEFAULT 'not_started',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE INDEX IF NOT EXISTS ix_milestones_project_id_status ON milestones (project_id, status);

-- Check if column exists is hard in raw SQL script without logic, but we can try adding it and ignore error if possible, 
-- or just rely on the user running this once.
-- SQLite doesn't support "ADD COLUMN IF NOT EXISTS" directly in all versions.
-- We will assume it needs to be added if this script is run.

ALTER TABLE tasks ADD COLUMN milestone_id INTEGER REFERENCES milestones(id) ON DELETE SET NULL ON UPDATE CASCADE;

CREATE INDEX IF NOT EXISTS ix_tasks_milestone_id ON tasks (milestone_id);
