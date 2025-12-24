from typing import List, Optional, Any
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.dbmodels import Milestone, Task
from app.schemas.milestone import MilestoneCreate, MilestoneUpdate, MilestoneStatus, MilestoneProgress

class MilestoneService:
    @staticmethod
    def create(db: Session, obj_in: MilestoneCreate) -> Milestone:
        db_obj = Milestone(
            project_id=obj_in.project_id,
            name=obj_in.name,
            due_date=obj_in.due_date,
            status=MilestoneStatus.NOT_STARTED.value
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def get(db: Session, milestone_id: int) -> Optional[Milestone]:
        return db.query(Milestone).filter(Milestone.id == milestone_id).first()

    @staticmethod
    def get_by_project(db: Session, project_id: int) -> List[Milestone]:
        return db.query(Milestone).filter(Milestone.project_id == project_id).all()

    @staticmethod
    def update(db: Session, milestone_id: int, obj_in: MilestoneUpdate) -> Optional[Milestone]:
        db_obj = MilestoneService.get(db, milestone_id)
        if not db_obj:
            return None

        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        # Recalculate status in case Due Date changed
        MilestoneService.update_status(db, db_obj)

        return db_obj

    @staticmethod
    def delete(db: Session, milestone_id: int) -> bool:
        db_obj = MilestoneService.get(db, milestone_id)
        if not db_obj:
            return False
        db.delete(db_obj)
        db.commit()
        return True

    @staticmethod
    def calculate_progress(db: Session, milestone_id: int) -> MilestoneProgress:
        tasks = db.query(Task).filter(Task.milestone_id == milestone_id).all()
        total = len(tasks)
        if total == 0:
            return MilestoneProgress(
                total_tasks=0,
                completed_tasks=0,
                in_progress_tasks=0,
                todo_tasks=0,
                completion_percentage=0.0
            )

        completed = sum(1 for t in tasks if t.status == "done")
        in_progress = sum(1 for t in tasks if t.status == "in_progress")
        todo = sum(1 for t in tasks if t.status == "todo")

        return MilestoneProgress(
            total_tasks=total,
            completed_tasks=completed,
            in_progress_tasks=in_progress,
            todo_tasks=todo,
            completion_percentage=round((completed / total) * 100, 2)
        )

    @staticmethod
    def update_status(db: Session, milestone: Milestone) -> Milestone:
        # Determine status based on tasks and due date
        # Logic:
        # 1. If overdue and not completed -> OVERDUE
        # 2. If 100% completed -> COMPLETED
        # 3. If started (>0 completed or in_progress) -> IN_PROGRESS
        # 4. Else -> NOT_STARTED

        # We need fresh stats
        progress = MilestoneService.calculate_progress(db, milestone.id)

        new_status = MilestoneStatus.NOT_STARTED

        if progress.total_tasks > 0 and progress.completion_percentage == 100:
            new_status = MilestoneStatus.COMPLETED
        elif progress.completed_tasks > 0 or progress.in_progress_tasks > 0:
            new_status = MilestoneStatus.IN_PROGRESS

        # Check Overdue (Only if not completed)
        if new_status != MilestoneStatus.COMPLETED and milestone.due_date:
            # naive comparison vs timezone aware - ensure consistency
            now = datetime.now(milestone.due_date.tzinfo) if milestone.due_date.tzinfo else datetime.now()
            if now > milestone.due_date:
                 new_status = MilestoneStatus.OVERDUE

        if milestone.status != new_status.value:
            milestone.status = new_status.value
            db.add(milestone)
            db.commit()
            db.refresh(milestone)

        return milestone
