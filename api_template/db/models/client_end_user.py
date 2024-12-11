from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship

from api_template.db.base import Base
import enum


class EndUserStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    BLOCKED = "blocked"


class ClientEndUser(Base):
    __tablename__ = "client_end_users"

    id = Column(String(36), primary_key=True)
    client_id = Column(String(36), ForeignKey("clients.id"), nullable=False)
    agent_id = Column(String(36), ForeignKey("client_users.id"))
    name = Column(String(255), nullable=False)
    email = Column(String(255))
    phone_number = Column(String(20), nullable=False)
    additional_info = Column(JSON)
    status = Column(Enum(EndUserStatus), default=EndUserStatus.ACTIVE)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    client = relationship("Client", back_populates="end_users")
    agent = relationship("ClientUser", back_populates="end_users")
    sessions = relationship("Session", back_populates="end_user")
    events = relationship("Event", back_populates="end_user")
    calls = relationship("Call", back_populates="end_user")

def setup_relationships():
    ClientEndUser.client = relationship("Client", back_populates="end_users")
    ClientEndUser.sessions = relationship("Session", back_populates="end_user")
    ClientEndUser.events = relationship("Event", back_populates="end_user")
    ClientEndUser.calls = relationship("Call", back_populates="end_user")
