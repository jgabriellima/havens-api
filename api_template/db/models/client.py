from datetime import datetime
from sqlalchemy import Column, String, DateTime, JSON
from sqlalchemy.orm import relationship

from api_template.db.base import Base
from api_template.db.models.client_end_user import ClientEndUser
from api_template.db.models.associations import client_assistant_association


class Client(Base):
    __tablename__ = "clients"

    id = Column(String, primary_key=True)
    name = Column(String(255), nullable=False)
    additional_info = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    users = relationship("ClientUser", back_populates="client")
    end_users = relationship("ClientEndUser", back_populates="client")
    channels = relationship("CommunicationChannel", back_populates="client")
    assistants = relationship(
        "Assistant",
        secondary=client_assistant_association,
        back_populates="clients"
    )
    sessions = relationship("Session", back_populates="client")
    events = relationship("Event", back_populates="client")
    calls = relationship("Call", back_populates="client")

# Configuração tardia dos relacionamentos
def setup_relationships():
    Client.assistants = relationship(
        "Assistant",
        secondary=client_assistant_association,
        back_populates="clients"
    )
    Client.events = relationship("Event", back_populates="client")
    Client.calls = relationship("Call", back_populates="client")
