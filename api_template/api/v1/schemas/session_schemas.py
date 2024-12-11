from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class SessionCreate(BaseModel):
    client_id: str
    end_user_id: str
    channel_id: Optional[str] = None
    user_id: Optional[str] = None
    assistant_id: Optional[str] = None
    livekit_room_id: Optional[str] = None

class SessionUpdate(BaseModel):
    end_user_id: Optional[str] = None
    end_time: Optional[datetime] = None

class Session(BaseModel):
    id: str
    client_id: str
    channel_id: str
    user_id: str
    end_user_id: str
    assistant_id: str
    livekit_room_id: str
    start_time: datetime
    end_time: Optional[datetime] = None

    class Config:
        from_attributes = True 