from typing import List
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from api_template.api.v1.schemas import call_schemas
from api_template.api.v1.services.call_service import CallService
from api_template.db.session import get_db

router = APIRouter()

@router.post("/calls/outbound", response_model=call_schemas.Call)
async def initiate_call(
    call: call_schemas.CallCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    service = CallService(db)
    return await service.initiate_call(call, background_tasks)

@router.get("/sessions/{session_id}/calls/", response_model=List[call_schemas.Call])
def list_session_calls(
    session_id: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    service = CallService(db)
    return service.get_session_calls(session_id, skip=skip, limit=limit)

@router.post("/calls/{call_id}/end")
async def end_call(
    call_id: str,
    db: Session = Depends(get_db)
):
    service = CallService(db)
    return await service.end_call(call_id)

@router.get("/calls/{call_id}/status", response_model=call_schemas.CallStatus)
def get_call_status(call_id: str, db: Session = Depends(get_db)):
    service = CallService(db)
    return service.get_call_status(call_id) 