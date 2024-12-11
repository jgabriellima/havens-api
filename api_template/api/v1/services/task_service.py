from typing import List, Optional
from sqlalchemy.orm import Session
from api_template.api.v1.repositories.task_repository import TaskRepository
from api_template.api.v1.schemas import task_schemas
from fastapi import HTTPException

class TaskService:
    def __init__(self, db: Session):
        self.repository = TaskRepository(db)

    def create_task(self, task: task_schemas.TaskCreate) -> task_schemas.Task:
        return self.repository.create(task)

    def get_task(self, task_id: str) -> task_schemas.Task:
        task = self.repository.get_by_id(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task

    def get_tasks(self, skip: int = 0, limit: int = 100) -> List[task_schemas.Task]:
        return self.repository.get_all(skip=skip, limit=limit)

    def get_session_tasks(self, session_id: str, skip: int = 0, limit: int = 100) -> List[task_schemas.Task]:
        return self.repository.get_by_session(session_id, skip=skip, limit=limit)

    def update_task(self, task_id: str, task_update: task_schemas.TaskUpdate) -> task_schemas.Task:
        task = self.repository.update(task_id, task_update)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task

    def delete_task(self, task_id: str) -> bool:
        if not self.repository.delete(task_id):
            raise HTTPException(status_code=404, detail="Task not found")
        return True 