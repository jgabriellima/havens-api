from typing import List, Optional
from sqlalchemy.orm import Session
from uuid import uuid4

from api_template.db.models.assistant import Assistant, client_assistant_association
from api_template.api.v1.schemas import assistant_schemas

class AssistantRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, assistant: assistant_schemas.AssistantCreate) -> Assistant:
        db_assistant = Assistant(
            name=assistant.name,
            description=assistant.description,
            model=assistant.model,
            instructions=assistant.instructions,
            # Novos campos
            specialization=assistant.specialization,
            implementation_reference=assistant.implementation_reference
        )
        self.db_session.add(db_assistant)
        self.db_session.commit()
        self.db_session.refresh(db_assistant)
        return db_assistant

    def get_by_id(self, assistant_id: str) -> Optional[Assistant]:
        return self.db_session.query(Assistant)\
            .filter(Assistant.id == assistant_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Assistant]:
        return self.db_session.query(Assistant)\
            .offset(skip).limit(limit).all()

    def associate_with_client(self, client_id: str, assistant_id: str) -> dict:
        self.db_session.execute(
            client_assistant_association.insert().values(
                client_id=client_id,
                assistant_id=assistant_id
            )
        )
        self.db_session.commit()
        return {"client_id": client_id, "assistant_id": assistant_id}

    def get_client_assistants(self, client_id: str) -> List[Assistant]:
        return self.db_session.query(Assistant)\
            .join(client_assistant_association)\
            .filter(client_assistant_association.c.client_id == client_id)\
            .all()

    def remove_client_association(self, client_id: str, assistant_id: str) -> bool:
        result = self.db_session.execute(
            client_assistant_association.delete().where(
                client_assistant_association.c.client_id == client_id,
                client_assistant_association.c.assistant_id == assistant_id
            )
        )
        self.db_session.commit()
        return result.rowcount > 0 