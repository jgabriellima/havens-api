import re
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, validator


class UserBase(BaseModel):
    email: EmailStr = Field(..., description="User's email address")
    username: str = Field(..., min_length=3, max_length=50, description="User's username")
    first_name: Optional[str] = Field(None, max_length=50, description="User's first name")
    last_name: Optional[str] = Field(None, max_length=50, description="User's last name")

    @validator("username")
    def username_alphanumeric(cls, v):
        if not re.match(r"^[a-zA-Z0-9_]+$", v):
            raise ValueError("Username must be alphanumeric")
        return v


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="User's password")

    @validator("password")
    def password_strength(cls, v):
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError("Password must contain at least one special character")
        return v


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    password: Optional[str] = Field(None, min_length=8)


class UserInDB(UserBase):
    id: int
    is_active: bool = Field(default=True, description="Whether the user is active")
    hashed_password: str

    class Config:
        from_attributes = True


class UserResponse(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True


class TokenData(BaseModel):
    username: Optional[str] = None


# Base User Schema
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    is_active: bool = True


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    id: int
    
    class Config:
        from_attributes = True


# Internal User Schemas
class InternalUserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str
    role: str  # 'admin' or 'staff'
    department: Optional[str] = None
    is_active: bool = True

class InternalUserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: str
    department: Optional[str]
    is_active: bool

    class Config:
        from_attributes = True

# Client User Schemas
class ClientUserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str
    client_id: int  # ID do cliente ao qual o usuário estará vinculado
    company_name: str
    business_type: Optional[str] = None
    is_active: bool = True
    role: str = "client"

class ClientUserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    client_id: int
    company_name: str
    business_type: Optional[str]
    is_active: bool

    class Config:
        from_attributes = True

# End User Schemas
class EndUserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str
    preferences: Optional[dict] = None
    is_active: bool = True
    role: str = "end_user"

class EndUserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    preferences: Optional[dict]
    is_active: bool

    class Config:
        from_attributes = True
