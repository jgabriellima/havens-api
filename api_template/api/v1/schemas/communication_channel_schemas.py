from datetime import datetime
from enum import Enum
from pydantic import BaseModel
from typing import Optional

class ChannelType(str, Enum):
    WHATSAPP = "whatsapp"
    VOICE = "voice"
    SMS = "sms"
    EMAIL = "email"

class ChannelStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    MAINTENANCE = "maintenance"

class CommunicationChannelBase(BaseModel):
    channel_type: ChannelType
    channel_identifier: str

class CommunicationChannelCreate(CommunicationChannelBase):
    client_id: str

class CommunicationChannelUpdate(BaseModel):
    status: Optional[ChannelStatus]
    channel_identifier: Optional[str]

class CommunicationChannel(CommunicationChannelBase):
    id: str
    client_id: str
    status: ChannelStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 