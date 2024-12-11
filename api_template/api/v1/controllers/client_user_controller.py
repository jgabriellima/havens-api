from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api_template.api.v1.schemas import client_user_schemas
from api_template.api.v1.services.client_user_service import ClientUserService
from api_template.db.session import get_db

router = APIRouter()

# Usuários Internos (ClientUsers)
@router.post("/clients/{client_id}/users/", response_model=client_user_schemas.ClientUser)
def create_internal_user(
    client_id: str,
    user: client_user_schemas.ClientUserCreate,
    db: Session = Depends(get_db)
):
    """Criar usuário interno (corretor, administrador)"""
    service = ClientUserService(db)
    return service.create_internal_user(client_id, user)

@router.get("/clients/{client_id}/users/", response_model=List[client_user_schemas.ClientUser])
def list_internal_users(
    client_id: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Listar usuários internos do cliente"""
    service = ClientUserService(db)
    return service.get_internal_users(client_id, skip=skip, limit=limit)

# Usuários-Clientes (ClientEndUsers)
@router.post("/clients/{client_id}/end-users/", response_model=client_user_schemas.ClientEndUser)
def create_end_user(
    client_id: str,
    user: client_user_schemas.ClientEndUserCreate,
    db: Session = Depends(get_db)
):
    """Criar usuário-cliente (comprador, investidor)"""
    service = ClientUserService(db)
    return service.create_end_user(client_id, user)

@router.get("/clients/{client_id}/end-users/", response_model=List[client_user_schemas.ClientEndUser])
def list_end_users(
    client_id: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Listar usuários-clientes"""
    service = ClientUserService(db)
    return service.get_end_users(client_id, skip=skip, limit=limit)

# Operações comuns para ambos os tipos
@router.get("/clients/{client_id}/users/{user_id}", response_model=client_user_schemas.ClientUser)
def get_internal_user(client_id: str, user_id: str, db: Session = Depends(get_db)):
    service = ClientUserService(db)
    return service.get_internal_user(client_id, user_id)

@router.get("/clients/{client_id}/end-users/{user_id}", response_model=client_user_schemas.ClientEndUser)
def get_end_user(client_id: str, user_id: str, db: Session = Depends(get_db)):
    service = ClientUserService(db)
    return service.get_end_user(client_id, user_id) 