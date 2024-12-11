from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from enum import Enum

class SenderType(str, Enum):
    USER = "user"
    END_USER = "end_user"
    ASSISTANT = "assistant"

class ContentType(str, Enum):
    TEXT = "text"
    AUDIO = "audio"
    IMAGE = "image"
    VIDEO = "video"
    DOCUMENT = "document"

class MessageBase(BaseModel):
    sender_type: SenderType
    content_type: ContentType
    content: str

class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    id: str
    session_id: str
    timestamp: datetime

    class Config:
        from_attributes = True 