from datetime import datetime, timezone
from typing import Any, Dict

from app.dbmodels import GitContribution, LoggedHour, Task
from app.services.project import ProjectService
from sqlalchemy.orm import Session


class SummaryService:
    @staticmethod
    def generate_project_summary(db: Session, project_id: int) -> Dict[str, Any]:
        """
        Aggregates project data (tasks, commits, hours) into a structured summary.
        """
        # 1. Fetch Project
        project = ProjectService.get_project(db, project_id)
        if not project:
            # Note: Route will handle access check, but we need the project object
            return {}

        # 2. Tasks Aggregation
        tasks = db.query(Task).filter(Task.project_id == project_id).all()
        task_descriptions = [
            t.description for t in tasks if t.description and t.description.strip()
        ]

        task_count_by_status = {}
        for t in tasks:
            status = t.status or "unknown"
            task_count_by_status[status] = task_count_by_status.get(status, 0) + 1

        # 3. Git Contributions Aggregation
        commits = db.query(GitContribution).filter(GitContribution.project_id == project_id).all()
        commit_messages = [
            c.commit_message for c in commits if c.commit_message and c.commit_message.strip()
        ]

        # 4. Logged Hours Aggregation
        hours_entries = db.query(LoggedHour).filter(LoggedHour.project_id == project_id).all()
        logged_hour_notes = [h.note for h in hours_entries if h.note and h.note.strip()]
        total_hours = sum(h.hours for h in hours_entries)

        # 5. Date Range Calculation
        dates = []
        if tasks:
            dates.extend([t.created_at for t in tasks if t.created_at])
        if commits:
            dates.extend([c.created_at for c in commits if c.created_at])
        if hours_entries:
            dates.extend([h.logged_at for h in hours_entries if h.logged_at])

        earliest = min(dates) if dates else datetime.now(timezone.utc)
        latest = max(dates) if dates else datetime.now(timezone.utc)

        # 6. Generate Aggregated Text
        sections = []
        if task_descriptions:
            sections.append(
                "### Task Descriptions\n" + "\n".join(f"- {d}" for d in task_descriptions)
            )
        if commit_messages:
            sections.append("### Commit Messages\n" + "\n".join(f"- {m}" for m in commit_messages))
        if logged_hour_notes:
            sections.append(
                "### Logged Hour Notes\n" + "\n".join(f"- {n}" for n in logged_hour_notes)
            )

        aggregated_text = "\n\n".join(sections)

        # 7. Metadata
        metadata = {
            "total_tasks": len(tasks),
            "total_commits": len(commits),
            "total_logged_hours": int(total_hours),
            "date_range": {"earliest": earliest, "latest": latest},
            "task_count_by_status": task_count_by_status,
        }

        return {
            "project_id": project.id,
            "project_name": project.name,
            "task_descriptions": task_descriptions,
            "commit_messages": commit_messages,
            "logged_hour_notes": logged_hour_notes,
            "aggregated_text": aggregated_text,
            "metadata": metadata,
        }
