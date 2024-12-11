from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship

from api_template.db.base import Base
import enum


class UserRole(enum.Enum):
    ADMIN = "admin"
    AGENT = "agent"
    MANAGER = "manager"


class UserStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


class ClientUser(Base):
    __tablename__ = "client_users"

    id = Column(String(36), primary_key=True)
    client_id = Column(String(36), ForeignKey("clients.id"), nullable=False)
    name = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    phone_number = Column(String(20))
    external_user_id = Column(String(255))
    status = Column(Enum(UserStatus), default=UserStatus.ACTIVE)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    client = relationship("Client", back_populates="users")
    end_users = relationship("ClientEndUser", back_populates="agent")
    sessions = relationship("Session", back_populates="user")
    events = relationship("Event", back_populates="user")
    calls = relationship("Call", back_populates="user")


def setup_relationships():
    ClientUser.client = relationship("Client", back_populates="users")
    ClientUser.end_users = relationship("ClientEndUser", back_populates="agent")
    ClientUser.sessions = relationship("Session", back_populates="user")
    ClientUser.events = relationship("Event", back_populates="user")
    ClientUser.calls = relationship("Call", back_populates="user")
