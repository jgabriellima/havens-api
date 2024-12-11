from typing import List
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from api_template.api.v1.schemas import communication_channel_schemas, session_schemas, message_schemas
from api_template.api.v1.services.communication_channel_service import CommunicationChannelService
from api_template.api.v1.services.session_service import SessionService
from api_template.db.session import get_db

router = APIRouter()

# Canais de Comunicação
@router.post("/channels/", response_model=communication_channel_schemas.CommunicationChannel)
def create_channel(channel: communication_channel_schemas.CommunicationChannelCreate, db: Session = Depends(get_db)):
    service = CommunicationChannelService(db)
    return service.create_channel(channel)

@router.get("/clients/{client_id}/channels/", response_model=List[communication_channel_schemas.CommunicationChannel])
def list_client_channels(client_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = CommunicationChannelService(db)
    return service.get_channels_by_client(client_id, skip=skip, limit=limit)

@router.put("/channels/{channel_id}", response_model=communication_channel_schemas.CommunicationChannel)
def update_channel(channel_id: str, channel: communication_channel_schemas.CommunicationChannelUpdate, db: Session = Depends(get_db)):
    service = CommunicationChannelService(db)
    return service.update_channel(channel_id, channel)

# Webhook handlers para eventos externos
@router.post("/webhooks/whatsapp")
async def whatsapp_webhook(payload: dict, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    service = CommunicationChannelService(db)
    return await service.process_whatsapp_webhook(payload, background_tasks)

@router.post("/webhooks/voice")
async def voice_webhook(payload: dict, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    service = CommunicationChannelService(db)
    return await service.process_voice_webhook(payload, background_tasks) 