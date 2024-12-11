from typing import List
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from api_template.api.v1.schemas import message_schemas
from api_template.api.v1.services.message_service import MessageService
from api_template.db.session import get_db

router = APIRouter()

@router.post("/sessions/{session_id}/messages/", response_model=message_schemas.Message)
def create_message(
    session_id: str,
    message: message_schemas.MessageCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    service = MessageService(db)
    return service.create_message(session_id, message, background_tasks)

@router.get("/sessions/{session_id}/messages/", response_model=List[message_schemas.Message])
def list_session_messages(
    session_id: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    service = MessageService(db)
    return service.get_session_messages(session_id, skip=skip, limit=limit)

@router.post("/messages/{message_id}/process", response_model=message_schemas.Message)
async def process_message(
    message_id: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    service = MessageService(db)
    return await service.process_message(message_id, background_tasks) 