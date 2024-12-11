from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException

from api_template.api.v1.schemas import assistant_schemas
from api_template.db.models.assistant import Assistant
from api_template.db.models.associations import client_assistant_association

class AssistantService:
    def __init__(self, db: Session):
        self.db = db

    def create_assistant(self, assistant: assistant_schemas.AssistantCreate) -> Assistant:
        db_assistant = Assistant(
            name=assistant.name,
            description=assistant.description,
            model=assistant.model,
            instructions=assistant.instructions,
            specialization=assistant.specialization,
            implementation_reference=assistant.implementation_reference
        )
        self.db.add(db_assistant)
        self.db.commit()
        self.db.refresh(db_assistant)
        return db_assistant

    def get_assistants(self, skip: int = 0, limit: int = 100) -> List[Assistant]:
        return self.db.query(Assistant).offset(skip).limit(limit).all()

    def get_assistant(self, assistant_id: str) -> Assistant:
        assistant = self.db.query(Assistant).filter(Assistant.id == assistant_id).first()
        if not assistant:
            raise HTTPException(status_code=404, detail="Assistant not found")
        return assistant

    def associate_assistant(self, client_id: str, assistant_id: str) -> assistant_schemas.ClientAssistantAssociation:
        assistant = self.get_assistant(assistant_id)
        
        # Verificar se a associação já existe
        existing = self.db.query(client_assistant_association).filter_by(
            client_id=client_id,
            assistant_id=assistant_id
        ).first()
        
        if existing:
            raise HTTPException(status_code=400, detail="Association already exists")

        # Inserir na tabela de associação
        self.db.execute(
            client_assistant_association.insert().values(
                client_id=client_id,
                assistant_id=assistant_id
            )
        )
        self.db.commit()
        
        return assistant_schemas.ClientAssistantAssociation(
            client_id=client_id,
            assistant_id=assistant_id
        )

    def get_client_assistants(self, client_id: str) -> List[Assistant]:
        return self.db.query(Assistant).join(
            client_assistant_association
        ).filter(
            client_assistant_association.c.client_id == client_id
        ).all()

    def remove_association(self, client_id: str, assistant_id: str) -> dict:
        result = self.db.execute(
            client_assistant_association.delete().where(
                client_assistant_association.c.client_id == client_id,
                client_assistant_association.c.assistant_id == assistant_id
            )
        )
        
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Association not found")
        
        self.db.commit()
        return {"status": "success"} 