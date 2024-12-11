from typing import List, Optional
from sqlalchemy.orm import Session
from uuid import uuid4
from datetime import datetime

from api_template.db.models.event import Event
from api_template.api.v1.schemas import event_schemas

class EventRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, event: event_schemas.SystemEventCreate) -> Event:
        db_event = Event(
            id=str(uuid4()),
            session_id=event.session_id,
            event_type=event.event_type,
            event_data=event.event_data,
            timestamp=datetime.utcnow()
        )
        self.db_session.add(db_event)
        self.db_session.commit()
        self.db_session.refresh(db_event)
        return db_event

    def get_by_session(self, session_id: str, skip: int = 0, limit: int = 100) -> List[Event]:
        return self.db_session.query(Event)\
            .filter(Event.session_id == session_id)\
            .order_by(Event.timestamp.desc())\
            .offset(skip).limit(limit).all()

    def get_by_client(self, client_id: str, skip: int = 0, limit: int = 100) -> List[Event]:
        return self.db_session.query(Event)\
            .join(Event.session)\
            .filter(Event.session.has(client_id=client_id))\
            .order_by(Event.timestamp.desc())\
            .offset(skip).limit(limit).all()

    def create_task_event(self, event: event_schemas.TaskEventCreate) -> Event:
        db_event = Event(
            id=str(uuid4()),
            session_id=event.session_id,
            task_id=event.task_id,
            event_type=event.event_type,
            event_data=event.event_data,
            timestamp=datetime.utcnow()
        )
        self.db_session.add(db_event)
        self.db_session.commit()
        self.db_session.refresh(db_event)
        return db_event

    def create_session_event(self, event: event_schemas.SessionEventCreate) -> Event:
        db_event = Event(
            id=str(uuid4()),
            session_id=event.session_id,
            user_id=event.user_id,
            end_user_id=event.end_user_id,
            event_type=event.event_type,
            event_data=event.event_data,
            timestamp=datetime.utcnow()
        )
        self.db_session.add(db_event)
        self.db_session.commit()
        self.db_session.refresh(db_event)
        return db_event

    def get_event(self, event_id: str) -> Optional[Event]:
        return self.db_session.query(Event).filter(Event.id == event_id).first() 