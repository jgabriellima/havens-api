from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api_template.api.v1.schemas import task_schemas
from api_template.api.v1.services.task_service import TaskService
from api_template.db.session import get_db

router = APIRouter()

@router.post("/tasks/", response_model=task_schemas.Task)
def create_task(
    task: task_schemas.TaskCreate,
    db: Session = Depends(get_db)
):
    service = TaskService(db)
    return service.create_task(task)

@router.get("/tasks/{task_id}", response_model=task_schemas.Task)
def get_task(
    task_id: str,
    db: Session = Depends(get_db)
):
    service = TaskService(db)
    return service.get_task(task_id)

@router.get("/tasks/", response_model=List[task_schemas.Task])
def list_tasks(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    service = TaskService(db)
    return service.get_tasks(skip=skip, limit=limit)

@router.get("/sessions/{session_id}/tasks/", response_model=List[task_schemas.Task])
def list_session_tasks(
    session_id: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    service = TaskService(db)
    return service.get_session_tasks(session_id, skip=skip, limit=limit)

@router.put("/tasks/{task_id}", response_model=task_schemas.Task)
def update_task_status(
    task_id: str,
    task: task_schemas.TaskUpdate,
    db: Session = Depends(get_db)
):
    service = TaskService(db)
    return service.update_task(task_id, task)

@router.delete("/tasks/{task_id}")
def delete_task(
    task_id: str,
    db: Session = Depends(get_db)
):
    service = TaskService(db)
    return service.delete_task(task_id) 