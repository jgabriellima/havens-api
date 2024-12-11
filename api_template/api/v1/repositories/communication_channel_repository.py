from typing import List, Optional
from sqlalchemy.orm import Session
from uuid import uuid4

from api_template.db.models.communication_channel import CommunicationChannel
from api_template.api.v1.schemas import communication_channel_schemas

class CommunicationChannelRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, channel: communication_channel_schemas.CommunicationChannelCreate) -> CommunicationChannel:
        db_channel = CommunicationChannel(
            id=str(uuid4()),
            client_id=channel.client_id,
            channel_type=channel.channel_type,
            channel_identifier=channel.channel_identifier
        )
        self.db_session.add(db_channel)
        self.db_session.commit()
        self.db_session.refresh(db_channel)
        return db_channel

    def get_by_id(self, channel_id: str) -> Optional[CommunicationChannel]:
        return self.db_session.query(CommunicationChannel)\
            .filter(CommunicationChannel.id == channel_id).first()

    def get_by_client(self, client_id: str, skip: int = 0, limit: int = 100) -> List[CommunicationChannel]:
        return self.db_session.query(CommunicationChannel)\
            .filter(CommunicationChannel.client_id == client_id)\
            .offset(skip).limit(limit).all()

    def get_by_identifier(self, identifier: str) -> Optional[CommunicationChannel]:
        return self.db_session.query(CommunicationChannel)\
            .filter(CommunicationChannel.channel_identifier == identifier).first()

    def update(self, channel_id: str, 
              channel: communication_channel_schemas.CommunicationChannelUpdate) -> Optional[CommunicationChannel]:
        db_channel = self.get_by_id(channel_id)
        if db_channel:
            for field, value in channel.dict(exclude_unset=True).items():
                setattr(db_channel, field, value)
            self.db_session.commit()
            self.db_session.refresh(db_channel)
        return db_channel

    def delete(self, channel_id: str) -> bool:
        db_channel = self.get_by_id(channel_id)
        if db_channel:
            self.db_session.delete(db_channel)
            self.db_session.commit()
            return True
        return False 