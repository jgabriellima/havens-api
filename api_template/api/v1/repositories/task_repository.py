from typing import List, Optional
from sqlalchemy.orm import Session
from api_template.db.models.task import BackgroundTask
from api_template.api.v1.schemas import task_schemas
import uuid

class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, task: task_schemas.TaskCreate) -> BackgroundTask:
        db_task = BackgroundTask(
            id=str(uuid.uuid4()),
            task_type=task.task_type,
            status="pending",
            input_data=task.input_data,
            retry=task.retry
        )
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        return db_task

    def get_by_id(self, task_id: str) -> Optional[BackgroundTask]:
        return self.db.query(BackgroundTask).filter(BackgroundTask.id == task_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[BackgroundTask]:
        return self.db.query(BackgroundTask).offset(skip).limit(limit).all()

    def get_by_session(self, session_id: str, skip: int = 0, limit: int = 100) -> List[BackgroundTask]:
        return (
            self.db.query(BackgroundTask)
            .filter(BackgroundTask.session_id == session_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update(self, task_id: str, task_update: task_schemas.TaskUpdate) -> Optional[BackgroundTask]:
        db_task = self.get_by_id(task_id)
        if db_task:
            for key, value in task_update.dict(exclude_unset=True).items():
                setattr(db_task, key, value)
            self.db.commit()
            self.db.refresh(db_task)
        return db_task

    def delete(self, task_id: str) -> bool:
        db_task = self.get_by_id(task_id)
        if db_task:
            self.db.delete(db_task)
            self.db.commit()
            return True
        return False 