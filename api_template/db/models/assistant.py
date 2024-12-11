from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import uuid
from api_template.db.base import Base
from api_template.db.models.associations import client_assistant_association


def generate_uuid():
    return str(uuid.uuid4())


class Assistant(Base):
    __tablename__ = "assistants"

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    description = Column(String)
    model = Column(String, nullable=False)
    instructions = Column(String)
    specialization = Column(String)
    implementation_reference = Column(String)

# Configuração tardia dos relacionamentos
def setup_relationships():
    Assistant.clients = relationship(
        "Client",
        secondary=client_assistant_association,
        back_populates="assistants"
    )
    Assistant.sessions = relationship("Session", back_populates="assistant")


