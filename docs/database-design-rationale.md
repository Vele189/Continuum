## Continuum Database Design Rationale

This schema prioritizes data integrity, query performance, and operational flexibility using SQLAlchemy models for the SQLite backend.

### 1. Data Integrity and Referential Actions

Referential integrity is strictly enforced across all foreign keys (`ForeignKey`) using explicit `ON DELETE` and `ON UPDATE` rules:

| FK Rule | Location Examples | Rationale |
| :--- | :--- | :--- |
| **`ON DELETE CASCADE`** | `Project.client_id`, `Task.project_id`, `ProjectMember.project_id` | Core dependencies: Deleting a parent (e.g., a Client or Project) must automatically delete all associated children (e.g., Projects, Tasks, or Members) to prevent orphaned records. |
| **`ON DELETE SET NULL`** | `Task.assigned_to`, `Client.created_by`, `GitContribution.user_id` | Historical preservation: If a User is deleted, we keep the record (Task, Client, Commit) but clear the link, preserving history while removing the reference. |
| **`ON UPDATE CASCADE`** | Applied to **All Foreign Keys** | Ensures that if a Primary Key were ever changed, the update propagates consistently across all referencing tables. |

### 2. Constraints and Performance 

* **Primary Keys & Indexing:** All tables use an explicit `id` as the `PRIMARY KEY` and are indexed (`index=True`).
* **Unique Constraints:**
    * **User Identity:** `users.username` and `users.email` are enforced as unique for secure authentication.
    * **Activity Tracking:** `git_contributions.commit_hash` must be unique to prevent duplicate commit entries.
    * **Relationship Integrity:** The `ProjectMember` table uses a **Composite Unique Constraint** on `('project_id', 'user_id')` to ensure a single user cannot be added to the same project more than once.
* **Query Optimization:** Indexes are added to all Foreign Key columns (`project_id`, `user_id`, `client_id`) and frequently filtered status columns (`projects.status`, `tasks.status`) for fast joining and searching.

### 3. Nullability and Flexibility

* **Non-Nullable (`nullable=False`):** Enforced for critical fields that define the entity or relationship (`username`, `password_hash`, `project_id`, `hours`).
* **Nullable (`nullable=True`):** Used for non-essential detail fields (`description`, `note`) and for optional relationships, such as `logged_hours.task_id` (time can be logged directly against a project).
* **System Logs (`SystemLog.meta`):** Uses a `JSON` data type (or TEXT in SQLite) to allow for unstructured, extensible logging data (e.g., stack traces, request details) without requiring schema migrations.