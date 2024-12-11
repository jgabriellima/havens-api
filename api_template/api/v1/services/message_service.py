from typing import List
from fastapi import HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from api_template.api.v1.repositories.message_repository import MessageRepository
from api_template.api.v1.repositories.session_repository import SessionRepository
from api_template.api.v1.schemas import message_schemas

class MessageService:
    def __init__(self, db_session: Session):
        self.repository = MessageRepository(db_session)
        self.session_repository = SessionRepository(db_session)

    async def create_message(
        self, 
        session_id: str, 
        message: message_schemas.MessageCreate,
        background_tasks: BackgroundTasks
    ) -> message_schemas.Message:
        # Verificar se a sessão existe e está ativa
        session = self.session_repository.get_by_id(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        if session.end_time:
            raise HTTPException(status_code=400, detail="Session already ended")

        # Criar mensagem
        db_message = self.repository.create(session_id, message)

        # Se for mensagem de áudio, agendar transcrição
        if message.content_type == message_schemas.ContentType.AUDIO:
            background_tasks.add_task(self._process_audio, db_message.id)

        return db_message

    def get_session_messages(
        self, 
        session_id: str, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[message_schemas.Message]:
        return self.repository.get_by_session(session_id, skip=skip, limit=limit)

    async def process_message(
        self, 
        message_id: str,
        background_tasks: BackgroundTasks
    ) -> message_schemas.Message:
        message = self.repository.get_by_id(message_id)
        if not message:
            raise HTTPException(status_code=404, detail="Message not found")

        # Processar mensagem de acordo com o tipo
        if message.content_type == message_schemas.ContentType.AUDIO:
            background_tasks.add_task(self._process_audio, message.id)
        
        return message

    async def _process_audio(self, message_id: str):
        # Implementar lógica de processamento de áudio
        # Por exemplo: transcrição, análise de sentimento, etc.
        pass 