# Continuum Database Schema

This document outlines the foundational PostgreSQL database schema for the Continuum application.

---

### 1. `users` Table
**Purpose:** Stores information about application users, including their login credentials and hourly rate for billing/cost tracking.

| Field | Type | Constraint/Notes |
| :--- | :--- | :--- |
| **id** | INTEGER | PRIMARY KEY, AUTOINCREMENT |
| **username** | TEXT | UNIQUE, NOT NULL |
| **email** | TEXT | UNIQUE, NOT NULL |
| **password_hash** | TEXT | NOT NULL (Stores hashed password) |
| **display_name** | TEXT | NOT NULL |
| **hourly_rate** | REAL | Cost/Billing rate per hour (FLOAT) |
| **created_at** | TEXT | Timestamp of creation |

### 2. `clients` Table
**Purpose:** Stores records for the external clients/companies that Continuum does work for.

| Field | Type | Constraint/Notes |
| :--- | :--- | :--- |
| **id** | INTEGER | PRIMARY KEY, AUTOINCREMENT |
| **name** | TEXT | NOT NULL |
| **email** | TEXT | Client's main contact email |
| **created_by** | INTEGER | FOREIGN KEY to `users.id` |
| **created_at** | TEXT | Timestamp of creation |

### 3. `projects` Table
**Purpose:** Stores main project records, linking them to a client.

| Field | Type | Constraint/Notes |
| :--- | :--- | :--- |
| **id** | INTEGER | PRIMARY KEY, AUTOINCREMENT |
| **client_id** | INTEGER | FOREIGN KEY to `clients.id` |
| **name** | TEXT | NOT NULL |
| **description** | TEXT | |
| **status** | TEXT | e.g., 'Active', 'Completed', 'On Hold' |
| **created_at** | TEXT | Timestamp of creation |

### 4. `project_members` Table
**Purpose:** A join table to associate users with projects and define their role within that project.

| Field | Type | Constraint/Notes |
| :--- | :--- | :--- |
| **id** | INTEGER | PRIMARY KEY, AUTOINCREMENT |
| **project_id** | INTEGER | FOREIGN KEY to `projects.id` |
| **user_id** | INTEGER | FOREIGN KEY to `users.id` |
| **role** | TEXT | e.g., 'Manager', 'Developer' |
| **added_at** | TEXT | Timestamp user was added |

### 5. `tasks` Table
**Purpose:** Stores individual work items/tasks within a project.

| Field | Type | Constraint/Notes |
| :--- | :--- | :--- |
| **id** | INTEGER | PRIMARY KEY, AUTOINCREMENT |
| **project_id** | INTEGER | FOREIGN KEY to `projects.id` |
| **title** | TEXT | NOT NULL |
| **description** | TEXT | |
| **status** | TEXT | e.g., 'To Do', 'In Progress', 'Done' |
| **assigned_to** | INTEGER | FOREIGN KEY to `users.id` (assignee) |
| **created_at** | TEXT | Timestamp of creation |
| **updated_at** | TEXT | Timestamp of last update |

### 6. `logged_hours` Table
**Purpose:** Stores records of time logged by users against a specific task or project.

| Field | Type | Constraint/Notes |
| :--- | :--- | :--- |
| **id** | INTEGER | PRIMARY KEY, AUTOINCREMENT |
| **user_id** | INTEGER | FOREIGN KEY to `users.id` |
| **task_id** | INTEGER | FOREIGN KEY to `tasks.id` (Can be NULL if logging against project only) |
| **project_id** | INTEGER | FOREIGN KEY to `projects.id` |
| **hours** | REAL | NOT NULL (Logged hours, FLOAT) |
| **note** | TEXT | Description of work done |
| **logged_at** | TEXT | Timestamp of when the time was logged |

### 7. `git_contributions` Table
**Purpose:** Stores records of git commits/contributions made by users to projects for traceability.

| Field | Type | Constraint/Notes |
| :--- | :--- | :--- |
| **id** | INTEGER | PRIMARY KEY, AUTOINCREMENT |
| **user_id** | INTEGER | FOREIGN KEY to `users.id` |
| **project_id** | INTEGER | FOREIGN KEY to `projects.id` |
| **commit_hash** | TEXT | UNIQUE, NOT NULL |
| **commit_message** | TEXT | |
| **branch** | TEXT | e.g., 'main', 'feature/x' |
| **committed_at** | TEXT | Timestamp of commit |

### 8. `system_logs` Table
**Purpose:** Stores internal system events, errors, and informational messages.

| Field | Type | Constraint/Notes |
| :--- | :--- | :--- |
| **id** | INTEGER | PRIMARY KEY, AUTOINCREMENT |
| **level** | TEXT | e.g., 'INFO', 'WARNING', 'ERROR' |
| **message** | TEXT | NOT NULL |
| **meta** | TEXT | Store complex data (e.g., JSON string) |
| **created_at** | TEXT | Timestamp of log event |
