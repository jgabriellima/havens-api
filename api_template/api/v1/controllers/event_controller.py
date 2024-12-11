from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api_template.api.v1.schemas import event_schemas
from api_template.api.v1.services.event_service import EventService
from api_template.db.session import get_db

router = APIRouter()

@router.get("/sessions/{session_id}/events/", response_model=List[event_schemas.Event])
def list_session_events(
    session_id: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    service = EventService(db)
    return service.get_session_events(session_id, skip=skip, limit=limit)

@router.get("/clients/{client_id}/events/", response_model=List[event_schemas.Event])
def list_client_events(
    client_id: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    service = EventService(db)
    return service.get_client_events(client_id, skip=skip, limit=limit)

@router.post("/events/system", response_model=event_schemas.Event)
def create_system_event(
    event: event_schemas.SystemEventCreate,
    db: Session = Depends(get_db)
):
    service = EventService(db)
    return service.create_system_event(event)

@router.post("/events/task", response_model=event_schemas.Event)
def create_task_event(
    event: event_schemas.TaskEventCreate,
    db: Session = Depends(get_db)
):
    service = EventService(db)
    return service.create_task_event(event)

@router.post("/events/session", response_model=event_schemas.Event)
def create_session_event(
    event: event_schemas.SessionEventCreate,
    db: Session = Depends(get_db)
):
    service = EventService(db)
    return service.create_session_event(event)

@router.get("/events/{event_id}", response_model=event_schemas.Event)
def get_event(
    event_id: str,
    db: Session = Depends(get_db)
):
    service = EventService(db)
    event = service.get_event(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event 