from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

# Schemas para Usuários Internos (ClientUsers)
class ClientUserBase(BaseModel):
    user_name: str
    email: EmailStr
    phone_number: str
    user_role: str  # 'Administrador', 'Corretor'
    external_user_id: Optional[str] = None
    status: str = "active"

class ClientUserCreate(ClientUserBase):
    password: str

class ClientUser(ClientUserBase):
    id: int
    client_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Schemas para Usuários-Clientes (ClientEndUsers)
class ClientEndUserBase(BaseModel):
    name: str
    email: EmailStr
    phone_number: str
    additional_info: Optional[dict] = None
    status: str = "active"

class ClientEndUserCreate(ClientEndUserBase):
    user_id: int  # Referência ao corretor responsável

class ClientEndUser(ClientEndUserBase):
    id: int
    client_id: str
    user_id: int  # Referência ao corretor responsável
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 

class ClientUserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    role: Optional[str] = None
    external_user_id: Optional[str] = None
    status: Optional[str] = None
    
    class Config:
        from_attributes = True 