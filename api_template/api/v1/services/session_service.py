from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from api_template.api.v1.repositories.session_repository import SessionRepository
from api_template.api.v1.schemas import session_schemas

class SessionService:
    def __init__(self, db_session: Session):
        self.repository = SessionRepository(db_session)

    def create_session(self, session: session_schemas.SessionCreate) -> session_schemas.Session:
        # Verificar se já existe uma sessão ativa para o mesmo end_user
        if session.end_user_id:
            active_sessions = self.repository.get_active_by_client(session.client_id)
            for active in active_sessions:
                if active.end_user_id == session.end_user_id:
                    # Encerrar sessão anterior
                    self.end_session(active.id)
        
        return self.repository.create(session)

    def get_session(self, session_id: str) -> session_schemas.Session:
        session = self.repository.get_by_id(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        return session

    def get_active_sessions(self, client_id: str) -> List[session_schemas.Session]:
        return self.repository.get_active_by_client(client_id)

    def get_sessions_by_client(self, client_id: str, skip: int = 0, limit: int = 100) -> List[session_schemas.Session]:
        return self.repository.get_by_client(client_id, skip=skip, limit=limit)

    def end_session(self, session_id: str) -> session_schemas.Session:
        session = self.repository.end_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        return session

    def update_session(self, session_id: str, session: session_schemas.SessionUpdate) -> session_schemas.Session:
        updated_session = self.repository.update(session_id, session)
        if not updated_session:
            raise HTTPException(status_code=404, detail="Session not found")
        return updated_session 