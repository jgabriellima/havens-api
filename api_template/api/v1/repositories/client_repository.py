from typing import List, Optional
from sqlalchemy.orm import Session
from uuid import uuid4

from api_template.db.models.client import Client
from api_template.api.v1.schemas import client_schemas

class ClientRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, client: client_schemas.ClientCreate) -> Client:
        db_client = Client(
            id=str(uuid4()),
            name=client.name,
            additional_info=client.additional_info
        )
        self.db_session.add(db_client)
        self.db_session.commit()
        self.db_session.refresh(db_client)
        return db_client

    def get_by_id(self, client_id: str) -> Optional[Client]:
        return self.db_session.query(Client).filter(Client.id == client_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Client]:
        return self.db_session.query(Client).offset(skip).limit(limit).all()

    def update(self, client_id: str, client: client_schemas.ClientUpdate) -> Optional[Client]:
        db_client = self.get_by_id(client_id)
        if db_client:
            for field, value in client.dict(exclude_unset=True).items():
                setattr(db_client, field, value)
            self.db_session.commit()
            self.db_session.refresh(db_client)
        return db_client

    def delete(self, client_id: str) -> bool:
        db_client = self.get_by_id(client_id)
        if db_client:
            self.db_session.delete(db_client)
            self.db_session.commit()
            return True
        return False 