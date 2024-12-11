from typing import List, Optional
from sqlalchemy.orm import Session
from uuid import uuid4

from api_template.db.models.client_user import ClientUser
from api_template.api.v1.schemas import client_user_schemas

class ClientUserRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, user: client_user_schemas.ClientUserCreate) -> ClientUser:
        db_user = ClientUser(
            id=str(uuid4()),
            client_id=user.client_id,
            name=user.name,
            role=user.role,
            email=user.email,
            phone_number=user.phone_number,
            external_user_id=user.external_user_id
        )
        self.db_session.add(db_user)
        self.db_session.commit()
        self.db_session.refresh(db_user)
        return db_user

    def get_by_id(self, user_id: str) -> Optional[ClientUser]:
        return self.db_session.query(ClientUser).filter(ClientUser.id == user_id).first()

    def get_by_email(self, email: str) -> Optional[ClientUser]:
        return self.db_session.query(ClientUser).filter(ClientUser.email == email).first()

    def get_by_client(self, client_id: str, skip: int = 0, limit: int = 100) -> List[ClientUser]:
        return self.db_session.query(ClientUser)\
            .filter(ClientUser.client_id == client_id)\
            .offset(skip).limit(limit).all()

    def update(self, user_id: str, user: client_user_schemas.ClientUserUpdate) -> Optional[ClientUser]:
        db_user = self.get_by_id(user_id)
        if db_user:
            for field, value in user.dict(exclude_unset=True).items():
                setattr(db_user, field, value)
            self.db_session.commit()
            self.db_session.refresh(db_user)
        return db_user

    def delete(self, user_id: str) -> bool:
        db_user = self.get_by_id(user_id)
        if db_user:
            self.db_session.delete(db_user)
            self.db_session.commit()
            return True
        return False 