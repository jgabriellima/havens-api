from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class AssistantBase(BaseModel):
    name: str
    description: Optional[str] = None
    model: str
    instructions: Optional[str] = None
    specialization: Optional[str] = None
    implementation_reference: Optional[str] = None

class AssistantCreate(AssistantBase):
    pass

class Assistant(AssistantBase):
    id: str

    class Config:
        from_attributes = True

class ClientAssistantAssociation(BaseModel):
    client_id: str
    assistant_id: str

    class Config:
        from_attributes = True 