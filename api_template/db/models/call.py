from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship

from api_template.db.base import Base
import enum

class CallStatus(enum.Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class Call(Base):
    __tablename__ = "calls"

    id = Column(String(36), primary_key=True)
    session_id = Column(String(36), ForeignKey("sessions.id"), nullable=False)
    client_id = Column(String(36), ForeignKey("clients.id"), nullable=False)
    user_id = Column(String(36), ForeignKey("client_users.id"))
    end_user_id = Column(String(36), ForeignKey("client_end_users.id"))
    status = Column(Enum(CallStatus), nullable=False, default=CallStatus.SCHEDULED)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

def setup_relationships():
    Call.session = relationship("Session", back_populates="calls")
    Call.client = relationship("Client", back_populates="calls")
    Call.user = relationship("ClientUser", back_populates="calls")
    Call.end_user = relationship("ClientEndUser", back_populates="calls") 