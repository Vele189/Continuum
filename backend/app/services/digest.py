from datetime import datetime, timedelta

from app.dbmodels import GitContribution, LoggedHour, Task, User
from app.schemas.digest import CommitSummary, RiskItem, TaskSummary, UserHours, WeeklyDigest
from app.services.project import ProjectService
from sqlalchemy import func
from sqlalchemy.orm import Session


class DigestService:
    @staticmethod
    def generate_weekly_digest(db: Session, project_id: int, week_start: datetime) -> WeeklyDigest:
        """
        Generates a weekly project digest summarizing work, time, and git activity.
        """
        # 1. Access Check & Project Info
        # Using a dummy user_id=1 for now as the internal service call might need context,
        # but the route will pass the actual user info.
        project = ProjectService.get_project(db, project_id)
        if not project:
            # This check is usually handled by get_project_with_check in the route,
            # but we'll assume the project existence here.
            from fastapi import HTTPException

            raise HTTPException(status_code=404, detail="Project not found")

        week_end = week_start + timedelta(days=7)

        # 2. Completed Tasks
        completed_tasks_query = (
            db.query(Task)
            .filter(
                Task.project_id == project_id,
                Task.status.in_(["done", "completed"]),
                Task.updated_at >= week_start,
                Task.updated_at < week_end,
            )
            .all()
        )

        task_summaries = [
            TaskSummary(
                id=task.id, title=task.title, status=task.status, completed_at=task.updated_at
            )
            for task in completed_tasks_query
        ]

        # 3. Logged Hours
        hours_query = (
            db.query(
                LoggedHour.user_id,
                User.display_name,
                func.sum(LoggedHour.hours).label("total_hours"),
            )
            .join(User, LoggedHour.user_id == User.id)
            .filter(
                LoggedHour.project_id == project_id,
                LoggedHour.logged_at >= week_start,
                LoggedHour.logged_at < week_end,
            )
            .group_by(LoggedHour.user_id, User.display_name)
            .all()
        )

        total_hours_logged = sum((h.total_hours or 0.0) for h in hours_query)
        hours_breakdown = [
            UserHours(user_id=h.user_id, user_name=h.display_name, hours=h.total_hours or 0.0)
            for h in hours_query
        ]

        # 4. Git Contributions
        commits_query = (
            db.query(GitContribution)
            .filter(
                GitContribution.project_id == project_id,
                GitContribution.created_at >= week_start,
                GitContribution.created_at < week_end,
            )
            .all()
        )

        commit_summaries = []
        for commit in commits_query:
            # Try to get user name from commit if available, otherwise fallback
            author_name = "Unknown"
            if commit.user:
                author_name = commit.user.display_name

            commit_summaries.append(
                CommitSummary(
                    hash=commit.commit_hash,
                    message=commit.commit_message,
                    author_name=author_name,
                    created_at=commit.created_at,
                )
            )

        # 5. Milestone Progress Placeholder
        milestone_progress = {"note": "Milestone progress tracking to be implemented in phase 2"}

        # 6. Risks & Delays (Placeholder Only)
        risks_and_delays = [RiskItem(reason="Risk detection not implemented yet", severity="info")]

        return WeeklyDigest(
            project_id=project.id,
            project_name=project.name,
            week_start=week_start,
            week_end=week_end,
            completed_tasks=task_summaries,
            total_hours_logged=float(total_hours_logged),
            hours_breakdown=hours_breakdown,
            commits=commit_summaries,
            milestone_progress=milestone_progress,
            risks_and_delays=risks_and_delays,
        )
