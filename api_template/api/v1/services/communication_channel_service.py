from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session

from api_template.api.v1.repositories.communication_channel_repository import CommunicationChannelRepository
from api_template.api.v1.schemas import communication_channel_schemas

class CommunicationChannelService:
    def __init__(self, db_session: Session):
        self.repository = CommunicationChannelRepository(db_session)

    def create_channel(self, channel: communication_channel_schemas.CommunicationChannelCreate) -> communication_channel_schemas.CommunicationChannel:
        existing = self.repository.get_by_identifier(channel.channel_identifier)
        if existing:
            raise HTTPException(status_code=400, detail="Channel identifier already registered")
        return self.repository.create(channel)

    def get_channel(self, channel_id: str) -> communication_channel_schemas.CommunicationChannel:
        channel = self.repository.get_by_id(channel_id)
        if not channel:
            raise HTTPException(status_code=404, detail="Channel not found")
        return channel

    def get_channels_by_client(self, client_id: str, skip: int = 0, limit: int = 100) -> List[communication_channel_schemas.CommunicationChannel]:
        return self.repository.get_by_client(client_id, skip=skip, limit=limit)

    def update_channel(self, channel_id: str, channel: communication_channel_schemas.CommunicationChannelUpdate) -> communication_channel_schemas.CommunicationChannel:
        updated_channel = self.repository.update(channel_id, channel)
        if not updated_channel:
            raise HTTPException(status_code=404, detail="Channel not found")
        return updated_channel

    def delete_channel(self, channel_id: str) -> bool:
        if not self.repository.delete(channel_id):
            raise HTTPException(status_code=404, detail="Channel not found")
        return True 