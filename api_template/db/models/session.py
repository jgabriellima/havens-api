from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from api_template.db.base import Base
from api_template.db.models.task import BackgroundTask


class Session(Base):
    __tablename__ = "sessions"

    id = Column(String(36), primary_key=True)
    client_id = Column(String(36), ForeignKey("clients.id"), nullable=False)
    channel_id = Column(String(36), ForeignKey("communication_channels.id"), nullable=False)
    user_id = Column(String(36), ForeignKey("client_users.id"))
    end_user_id = Column(String(36), ForeignKey("client_end_users.id"))
    assistant_id = Column(String(36), ForeignKey("assistants.id"))
    livekit_room_id = Column(String(255))
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime)

def setup_relationships():
    Session.client = relationship("Client", back_populates="sessions")
    Session.channel = relationship("CommunicationChannel", back_populates="sessions")
    Session.user = relationship("ClientUser", back_populates="sessions")
    Session.end_user = relationship("ClientEndUser", back_populates="sessions")
    Session.assistant = relationship("Assistant", back_populates="sessions")
    Session.messages = relationship("Message", back_populates="session")
    Session.calls = relationship("Call", back_populates="session")
    Session.tasks = relationship("BackgroundTask", back_populates="session")
    Session.events = relationship("Event", back_populates="session")
