from datetime import datetime
from typing import Optional, Dict
from pydantic import BaseModel
from enum import Enum

class EventType(str, Enum):
    TASK_STARTED = "task_started"
    TASK_COMPLETED = "task_completed"
    SESSION_STARTED = "session_started"
    SESSION_ENDED = "session_ended"
    SYSTEM_ERROR = "system_error"
    SYSTEM_WARNING = "system_warning"

class EventBase(BaseModel):
    event_type: EventType
    event_data: Dict

class SystemEventCreate(EventBase):
    session_id: Optional[str] = None

class TaskEventCreate(EventBase):
    session_id: str
    task_id: str

class SessionEventCreate(EventBase):
    session_id: str
    user_id: Optional[str] = None
    end_user_id: Optional[str] = None

class Event(EventBase):
    id: str
    session_id: Optional[str]
    task_id: Optional[str]
    user_id: Optional[str]
    end_user_id: Optional[str]
    timestamp: datetime

    class Config:
        from_attributes = True 