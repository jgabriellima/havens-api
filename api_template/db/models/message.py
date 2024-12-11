from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship

from api_template.db.base import Base
import enum


class SenderType(enum.Enum):
    USER = "user"
    END_USER = "end_user"
    ASSISTANT = "assistant"


class ContentType(enum.Enum):
    TEXT = "text"
    AUDIO = "audio"
    IMAGE = "image"
    VIDEO = "video"
    DOCUMENT = "document"


class Message(Base):
    __tablename__ = "messages"

    id = Column(String(36), primary_key=True)
    session_id = Column(String(36), ForeignKey("sessions.id"), nullable=False)
    sender_type = Column(Enum(SenderType), nullable=False)
    content_type = Column(Enum(ContentType), nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationships
    session = relationship("Session", back_populates="messages")


def setup_relationships():
    Message.session = relationship("Session", back_populates="messages")
