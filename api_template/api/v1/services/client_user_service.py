from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session

from api_template.api.v1.repositories.client_user_repository import ClientUserRepository
from api_template.api.v1.schemas import client_user_schemas

class ClientUserService:
    def __init__(self, db_session: Session):
        self.repository = ClientUserRepository(db_session)

    def create_user(self, user: client_user_schemas.ClientUserCreate) -> client_user_schemas.ClientUser:
        if self.repository.get_by_email(user.email):
            raise HTTPException(status_code=400, detail="Email already registered")
        return self.repository.create(user)

    def get_user(self, user_id: str) -> client_user_schemas.ClientUser:
        user = self.repository.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def get_users_by_client(self, client_id: str, skip: int = 0, limit: int = 100) -> List[client_user_schemas.ClientUser]:
        return self.repository.get_by_client(client_id, skip=skip, limit=limit)

    def update_user(self, user_id: str, user: client_user_schemas.ClientUserUpdate) -> client_user_schemas.ClientUser:
        updated_user = self.repository.update(user_id, user)
        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found")
        return updated_user

    def delete_user(self, user_id: str) -> bool:
        if not self.repository.delete(user_id):
            raise HTTPException(status_code=404, detail="User not found")
        return True 