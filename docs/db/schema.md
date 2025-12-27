
# Continuum Database Schema Documentation

## Overview of Database Purpose

The Continuum database serves as the centralized, relational core for a modern project management and development tracking system. Its primary functions are to manage user accounts, client relationships, project structure, time logging, and automatically sync data from external services like Git. The design prioritizes data integrity and query performance for reporting.

# Database Schema Overview

This document lists all tables and fields currently implemented in the Continuum database.

## Tables

### users
Stores authentication and profile details for system users.
* `id`: Primary Key
* `username`: Unique login handle
* `email`: Unique email address
* `password_hash`: Hashed password
* `display_name`: Real name or alias
* `hourly_rate`: Default billing rate for the user
* `created_at`: Timestamp of registration

### clients
External entities (customers/companies) that projects belong to.
* `id`: Primary Key
* `name`: Client name
* `email`: Contact email
* `created_by`: FK to `users.id` (User who added the client)
* `created_at`: Timestamp

### projects
Work containers linked to a specific client.
* `id`: Primary Key
* `client_id`: FK to `clients.id`
* `name`: Project name
* `description`: Details
* `status`: Active, Archived, etc.
* `created_at`: Timestamp

### project_members
Junction table linking Users to Projects with specific roles.
* `id`: Primary Key
* `project_id`: FK to `projects.id`
* `user_id`: FK to `users.id`
* `role`: e.g., 'admin', 'developer'
* `added_at`: Timestamp

### tasks
Specific units of work within a project.
* `id`: Primary Key
* `project_id`: FK to `projects.id`
* `title`: Task summary
* `description`: Task details
* `status`: e.g., 'todo', 'in_progress'
* `assigned_to`: FK to `users.id`
* `created_at`: Timestamp
* `updated_at`: Timestamp (updates automatically)

### logged_hours
Time entries tracking work done.
* `id`: Primary Key
* `user_id`: FK to `users.id`
* `task_id`: FK to `tasks.id` (Optional)
* `project_id`: FK to `projects.id`
* `hours`: Amount of time logged
* `note`: Description of work
* `logged_at`: Timestamp

### git_contributions
Records of code commits linked to projects/users.
* `id`: Primary Key
* `user_id`: FK to `users.id`
* `project_id`: FK to `projects.id`
* `commit_hash`: Unique git hash
* `commit_message`: Git message
* `branch`: Git branch name
* `committed_at`: Timestamp from Git

### system_logs
General purpose application logging.
* `id`: Primary Key
* `level`: INFO, WARN, ERROR
* `message`: Log content
* `meta`: JSON field for extra context
* `created_at`: Timestamp



---

## Table-by-Table Breakdown

### 1. `users`
**Purpose:** Stores authentication and profile details for all system users.
| Field | Type | Key Fields | Relationships |
| :--- | :--- | :--- | :--- |
| `id` | PK | Primary identifier. | One-to-Many: Clients, Tasks (assigned), Hours, Git Contributions, Project Memberships. |
| `username` | String | **Unique**, Indexed | |
| `email` | String | **Unique**, Indexed | |
| `password_hash`| String | Non-nullable | |
| `display_name` | String | Non-nullable | |
| `hourly_rate` | Float | Billing rate (default 0.0). | |
| `created_at` | DateTime | Account creation timestamp. | |

### 2. `clients`
**Purpose:** External entities (customers/companies) that projects are billed to.
| Field | Type | Key Fields | Relationships |
| :--- | :--- | :--- | :--- |
| `id` | PK | Primary identifier. | One-to-Many: Projects. |
| `name` | String | Non-nullable | |
| `email` | String | Indexed | |
| `created_by` | FK `users.id` | User who added the client. | Many-to-One: User. **ON DELETE SET NULL**. |
| `created_at` | DateTime | Timestamp of creation. | |

### 3. `projects`
**Purpose:** Work containers linked to a specific client.
| Field | Type | Key Fields | Relationships |
| :--- | :--- | :--- | :--- |
| `id` | PK | Primary identifier. | One-to-Many: Tasks, Hours, Contributions, Members. |
| `client_id` | FK `clients.id` | The client this project is billed under. | Many-to-One: Client. **ON DELETE CASCADE**. |
| `name` | String | Non-nullable | |
| `description` | Text | Detailed scope of work. | |
| `status` | String | Indexed | |
| `created_at` | DateTime | Timestamp of project creation. | |

### 4. `project_members`
**Purpose:** Junction table linking Users to Projects and defining their role.
| Field | Type | Key Fields | Relationships |
| :--- | :--- | :--- | :--- |
| `id` | PK | Primary identifier for the relationship. | |
| `project_id`| FK `projects.id` | Project identifier. | Many-to-One: Project. **ON DELETE CASCADE**. |
| `user_id` | FK `users.id` | User identifier. | Many-to-One: User. **ON DELETE CASCADE**. |
| `role` | String | User's specific role on this project. | |
| `__table_args__`| Constraint | **Unique Constraint:** (`project_id`, `user_id`) | |

### 5. `tasks`
**Purpose:** Specific units of work that can be assigned and tracked.
| Field | Type | Key Fields | Relationships |
| :--- | :--- | :--- | :--- |
| `id` | PK | Primary identifier. | One-to-Many: Logged Hours. |
| `project_id`| FK `projects.id` | The project the task belongs to. | Many-to-One: Project. **ON DELETE CASCADE**. |
| `title` | String | Non-nullable | |
| `description` | Text | Task details. | |
| `status` | String | Indexed | |
| `assigned_to`| FK `users.id` | User responsible. | Many-to-One: User. **ON DELETE SET NULL**. |
| `created_at` | DateTime | Task creation timestamp. | |
| `updated_at` | DateTime | Last modification timestamp. | |

### 6. `logged_hours`
**Purpose:** Time entries tracking work performed by users.
| Field | Type | Key Fields | Relationships |
| :--- | :--- | :--- | :--- |
| `id` | PK | Primary identifier. | |
| `user_id` | FK `users.id` | User who logged the time. | Many-to-One: User. **ON DELETE CASCADE**. |
| `task_id` | FK `tasks.id` | Specific task worked on (optional). | Many-to-One: Task. **ON DELETE SET NULL**. |
| `project_id`| FK `projects.id` | Project billed against. | Many-to-One: Project. **ON DELETE CASCADE**. |
| `hours` | Float | Amount of time logged (non-nullable). | |
| `note` | Text | Detailed description of the work. | |
| `logged_at` | DateTime | Timestamp of the log entry. | |

### 7. `git_contributions`
**Purpose:** Records of code commits linked to projects and users.
| Field | Type | Key Fields | Relationships |
| :--- | :--- | :--- | :--- |
| `id` | PK | Primary identifier. | |
| `user_id` | FK `users.id` | User who made the commit. | Many-to-One: User. **ON DELETE SET NULL**. |
| `project_id`| FK `projects.id` | Project the code contributes to. | Many-to-One: Project. **ON DELETE CASCADE**. |
| `commit_hash`| String | **Unique**, Non-nullable | |
| `commit_message`| Text | The commit message. | |
| `branch` | String | The branch committed to. | |
| `committed_at`| DateTime | Timestamp from the commit metadata. | |

### 8. `system_logs`
**Purpose:** General purpose application logging for auditing and debugging.
| Field | Type | Key Fields | Relationships |
| :--- | :--- | :--- | :--- |
| `id` | PK | Primary identifier. | |
| `level` | String | Log severity (non-nullable). | |
| `message` | Text | Main log content (non-nullable). | |
| `meta` | JSON/Text | Structured context data. | |
| `created_at` | DateTime | Timestamp of the log entry. | |

---

## 4.Design Rationale Section

### Why certain relationships exist

The structure is centered on the **Project**, which acts as the core hub for all activity.

* **Cascading Ownership:** The relationships from `clients` to `projects` to `tasks` use `ON DELETE CASCADE` because a project cannot logically exist without a client, and tasks/members cannot exist without a project.
* **Historical Preservation:** Relationships involving user assignments (`tasks.assigned_to`, `clients.created_by`) use `ON DELETE SET NULL`. This ensures that if a user leaves the company and their account is deleted, the historical record of the task or the client creation remains intact, but the user reference is safely cleared.

### Why some fields are nullable / non-nullable

| Constraint | Fields | Rationale |
| :--- | :--- | :--- |
| **Non-Nullable** | `users.username`, `projects.client_id`, `logged_hours.hours` | These are critical fields defining the entity or a required relationship. Data entry is blocked if they are missing. |
| **Nullable** | `projects.description`, `logged_hours.note`, `tasks.assigned_to` | These fields are secondary details or optional assignments. They offer flexibility; for example, time can be logged against a project (`project_id` non-nullable) even if the user can't link it to a specific task (`task_id` nullable). |

### Assumptions made, Future extensibility, and Trade-offs

* **Assumptions:** We assume all time and date tracking should be **timezone-aware** (`DateTime(timezone=True)`). We assume `hourly_rate` is always a positive float (validation handled at the application layer).
* **Future Extensibility:** The use of the `meta` field (`JSON` or `TEXT`) in `system_logs` allows for adding any future diagnostic data without requiring schema migrations. The `role` string in `project_members` allows the application to define new access levels freely.
* **Trade-offs:** The use of **SQLAlchemy's ORM** helps handle complex schema changes automatically during migrations. PostgreSQL provides robust support for concurrent operations and production-grade performance.

### Constraints intentionally omitted (and why)

*   **`ON UPDATE CASCADE`**: Primary keys (`id`) in this system are immutable auto-incrementing integers. Changing a primary key is not a supported operation in our application logic, so cascading updates are unnecessary.
*   **Complex `CHECK` Constraints (e.g., `hours > 0`)**: While the database supports `CHECK` constraints, we have omitted them in the DDL in favor of validation at the Pydantic/Application layer (`app.schemas`). This allows for more user-friendly error messages and keeps the database schema portable and simple.
*   **Database-level Enum Constraints**: We use `VARCHAR` for status fields (`projects.status`, `tasks.status`) instead of native database ENUMs. This avoids migration complexities when adding new status types, as the valid values are strictly enforced by the application code (Python Enums).
