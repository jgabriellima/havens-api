from datetime import datetime
from typing import Optional, Dict, List
from pydantic import BaseModel, EmailStr

class ClientBase(BaseModel):
    name: str
    additional_info: Optional[Dict] = None

class ClientCreate(ClientBase):
    pass

class ClientUpdate(ClientBase):
    pass

class Client(ClientBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 