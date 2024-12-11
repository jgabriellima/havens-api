from typing import List, Optional
from sqlalchemy.orm import Session
from uuid import uuid4

from api_template.db.models.message import Message
from api_template.api.v1.schemas import message_schemas

class MessageRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, session_id: str, message: message_schemas.MessageCreate) -> Message:
        db_message = Message(
            id=str(uuid4()),
            session_id=session_id,
            sender_type=message.sender_type,
            content_type=message.content_type,
            content=message.content
        )
        self.db_session.add(db_message)
        self.db_session.commit()
        self.db_session.refresh(db_message)
        return db_message

    def get_by_id(self, message_id: str) -> Optional[Message]:
        return self.db_session.query(Message)\
            .filter(Message.id == message_id).first()

    def get_by_session(self, session_id: str, skip: int = 0, limit: int = 100) -> List[Message]:
        return self.db_session.query(Message)\
            .filter(Message.session_id == session_id)\
            .order_by(Message.timestamp.desc())\
            .offset(skip).limit(limit).all()

    def update(self, message_id: str, content: str) -> Optional[Message]:
        db_message = self.get_by_id(message_id)
        if db_message:
            db_message.content = content
            self.db_session.commit()
            self.db_session.refresh(db_message)
        return db_message 