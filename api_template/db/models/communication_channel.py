from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship

from api_template.db.base import Base
import enum


class ChannelType(enum.Enum):
    WHATSAPP = "whatsapp"
    VOICE = "voice"
    SMS = "sms"
    EMAIL = "email"


class ChannelStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    MAINTENANCE = "maintenance"


class CommunicationChannel(Base):
    __tablename__ = "communication_channels"

    id = Column(String(36), primary_key=True)
    client_id = Column(String(36), ForeignKey("clients.id"), nullable=False)
    channel_type = Column(Enum(ChannelType), nullable=False)
    channel_identifier = Column(String(255), nullable=False)
    status = Column(Enum(ChannelStatus), default=ChannelStatus.ACTIVE)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    client = relationship("Client", back_populates="channels")
    sessions = relationship("Session", back_populates="channel")

def setup_relationships():
    CommunicationChannel.sessions = relationship("Session", back_populates="channel")
