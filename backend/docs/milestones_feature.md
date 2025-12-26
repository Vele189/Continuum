# Milestones Feature Documentation

## Overview
The Milestones system allows projects to group tasks into deliverables and automatically track progress. It answers the question: **"How close are we to delivering this part of the project?"**

## Core Concepts

### Milestone Entity
A specific deliverable or phase within a project.
- **Attributes**: Name, Due Date, Status, Project Link.
- **Status**: `not_started`, `in_progress`, `completed`, `overdue`.
- **Progress**: Automatically calculated based on linked tasks.

### Task Linking
Tasks can be linked to a single milestone. Linking a task affects the milestone's progress and status.

## Architecture & Implementation

### Database Schema
- **Table**: `milestones`
- **Relationship**:
    - One-to-Many: Project -> Milestones
    - One-to-Many: Milestone -> Tasks (Task has `milestone_id`)

### Automatic Status Logic
- **Not Started**: 0 tasks completed.
- **In Progress**: >0 tasks completed but <100%.
- **Completed**: 100% of tasks completed.
- **Overdue**: Due date passed and not completed.

### API Surface
- `POST /api/v1/milestones`: Create a milestone.
- `GET /api/v1/milestones/{id}`: Get details + progress metrics.
- `GET /api/v1/projects/{id}/milestones`: List project milestones.
- `PATCH /api/v1/tasks/{id}`: Link task to milestone (via `milestone_id`).

## Usage Guide (Planned)

### Creating a Milestone
```json
POST /api/v1/milestones
{
  "project_id": 1,
  "name": "Alpha Release",
  "due_date": "2025-01-01T00:00:00Z"
}
```

### Checking Progress
```json
GET /api/v1/milestones/1
{
  "id": 1,
  "name": "Alpha Release",
  "status": "in_progress",
  "progress": {
    "total_tasks": 10,
    "completed_tasks": 5,
    "completion_percentage": 50.0
  }
}
```

## Migration Notes
- A migration script `scripts/migrate_milestones.py` is provided to update the database schema.
- This adds the `milestones` table and the `milestone_id` column to `tasks`.
