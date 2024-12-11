from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
from api_template.db.base import Base
import enum

class EventType(enum.Enum):
    MESSAGE = "message"
    CALL = "call"
    TASK = "task"
    SESSION = "session"
    SYSTEM = "system"

class Event(Base):
    __tablename__ = "events"

    id = Column(String(36), primary_key=True)
    session_id = Column(String(36), ForeignKey("sessions.id"), nullable=False)
    client_id = Column(String(36), ForeignKey("clients.id"), nullable=False)
    user_id = Column(String(36), ForeignKey("client_users.id"))
    end_user_id = Column(String(36), ForeignKey("client_end_users.id"))
    event_type = Column(Enum(EventType), nullable=False)
    event_data = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    task_id = Column(String(36), ForeignKey("background_tasks.id"), nullable=True)

def setup_relationships():
    Event.session = relationship("Session", back_populates="events")
    Event.client = relationship("Client", back_populates="events")
    Event.user = relationship("ClientUser", back_populates="events")
    Event.end_user = relationship("ClientEndUser", back_populates="events")
    Event.task = relationship("BackgroundTask", back_populates="events")