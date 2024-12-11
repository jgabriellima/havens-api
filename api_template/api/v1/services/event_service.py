from typing import List, Optional
from sqlalchemy.orm import Session
from api_template.api.v1.schemas import event_schemas
from api_template.db.models.event import Event
from uuid import uuid4

class EventService:
    def __init__(self, db: Session):
        self.db = db

    def get_session_events(self, session_id: str, skip: int = 0, limit: int = 100) -> List[Event]:
        return (
            self.db.query(Event)
            .filter(Event.session_id == session_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_client_events(self, client_id: str, skip: int = 0, limit: int = 100) -> List[Event]:
        return (
            self.db.query(Event)
            .filter(Event.client_id == client_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create_system_event(self, event: event_schemas.SystemEventCreate) -> Event:
        db_event = Event(
            id=str(uuid4()),
            type="system",
            description=event.description,
            metadata=event.metadata
        )
        self.db.add(db_event)
        self.db.commit()
        self.db.refresh(db_event)
        return db_event

    def create_task_event(self, event: event_schemas.TaskEventCreate) -> Event:
        db_event = Event(
            id=str(uuid4()),
            type="task",
            description=event.description,
            task_id=event.task_id,
            metadata=event.metadata
        )
        self.db.add(db_event)
        self.db.commit()
        self.db.refresh(db_event)
        return db_event

    def create_session_event(self, event: event_schemas.SessionEventCreate) -> Event:
        db_event = Event(
            id=str(uuid4()),
            type="session",
            description=event.description,
            session_id=event.session_id,
            metadata=event.metadata
        )
        self.db.add(db_event)
        self.db.commit()
        self.db.refresh(db_event)
        return db_event

    def get_event(self, event_id: str) -> Optional[Event]:
        return self.db.query(Event).filter(Event.id == event_id).first() 