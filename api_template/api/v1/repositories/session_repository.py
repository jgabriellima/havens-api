from typing import List, Optional
from sqlalchemy.orm import Session
from uuid import uuid4
from datetime import datetime

from api_template.db.models.session import Session as SessionModel
from api_template.api.v1.schemas import session_schemas

class SessionRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, session: session_schemas.SessionCreate) -> SessionModel:
        db_session = SessionModel(
            id=str(uuid4()),
            client_id=session.client_id,
            channel_id=session.channel_id,
            user_id=session.user_id,
            end_user_id=session.end_user_id,
            assistant_id=session.assistant_id,
            livekit_room_id=session.livekit_room_id,
            start_time=datetime.utcnow()
        )
        self.db_session.add(db_session)
        self.db_session.commit()
        self.db_session.refresh(db_session)
        return db_session

    def get_by_id(self, session_id: str) -> Optional[SessionModel]:
        return self.db_session.query(SessionModel)\
            .filter(SessionModel.id == session_id).first()

    def get_active_by_client(self, client_id: str) -> List[SessionModel]:
        return self.db_session.query(SessionModel)\
            .filter(SessionModel.client_id == client_id)\
            .filter(SessionModel.end_time.is_(None))\
            .all()

    def get_by_client(self, client_id: str, skip: int = 0, limit: int = 100) -> List[SessionModel]:
        return self.db_session.query(SessionModel)\
            .filter(SessionModel.client_id == client_id)\
            .offset(skip).limit(limit).all()

    def end_session(self, session_id: str) -> Optional[SessionModel]:
        db_session = self.get_by_id(session_id)
        if db_session and not db_session.end_time:
            db_session.end_time = datetime.utcnow()
            self.db_session.commit()
            self.db_session.refresh(db_session)
        return db_session

    def update(self, session_id: str, session: session_schemas.SessionUpdate) -> Optional[SessionModel]:
        db_session = self.get_by_id(session_id)
        if db_session:
            for field, value in session.dict(exclude_unset=True).items():
                setattr(db_session, field, value)
            self.db_session.commit()
            self.db_session.refresh(db_session)
        return db_session 