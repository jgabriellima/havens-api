from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session

from api_template.api.v1.repositories.client_repository import ClientRepository
from api_template.api.v1.schemas import client_schemas

class ClientService:
    def __init__(self, db_session: Session):
        self.repository = ClientRepository(db_session)

    def create_client(self, client: client_schemas.ClientCreate) -> client_schemas.Client:
        return self.repository.create(client)

    def get_client(self, client_id: str) -> client_schemas.Client:
        client = self.repository.get_by_id(client_id)
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")
        return client

    def get_clients(self, skip: int = 0, limit: int = 100) -> List[client_schemas.Client]:
        return self.repository.get_all(skip=skip, limit=limit)

    def update_client(self, client_id: str, client: client_schemas.ClientUpdate) -> client_schemas.Client:
        updated_client = self.repository.update(client_id, client)
        if not updated_client:
            raise HTTPException(status_code=404, detail="Client not found")
        return updated_client

    def delete_client(self, client_id: str) -> bool:
        if not self.repository.delete(client_id):
            raise HTTPException(status_code=404, detail="Client not found")
        return True 