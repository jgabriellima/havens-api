from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from enum import Enum

class CallDirection(str, Enum):
    INBOUND = "inbound"
    OUTBOUND = "outbound"

class CallStatus(str, Enum):
    INITIATED = "initiated"
    RINGING = "ringing"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class CallBase(BaseModel):
    direction: CallDirection
    sip_trunk_id: Optional[str] = None

class CallCreate(CallBase):
    session_id: str

class Call(CallBase):
    id: str
    session_id: str
    status: CallStatus
    start_time: datetime
    end_time: Optional[datetime]

    class Config:
        from_attributes = True 