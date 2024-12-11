from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api_template.api.v1.schemas import client_schemas
from api_template.api.v1.services.client_service import ClientService
from api_template.db.session import get_db

router = APIRouter()

@router.post("/clients/", response_model=client_schemas.Client)
def create_client(client: client_schemas.ClientCreate, db: Session = Depends(get_db)):
    service = ClientService(db)
    return service.create_client(client)

@router.get("/clients/", response_model=List[client_schemas.Client])
def list_clients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = ClientService(db)
    return service.get_clients(skip=skip, limit=limit)

@router.get("/clients/{client_id}", response_model=client_schemas.Client)
def get_client(client_id: str, db: Session = Depends(get_db)):
    service = ClientService(db)
    return service.get_client(client_id)

@router.put("/clients/{client_id}", response_model=client_schemas.Client)
def update_client(client_id: str, client: client_schemas.ClientUpdate, db: Session = Depends(get_db)):
    service = ClientService(db)
    return service.update_client(client_id, client)

@router.delete("/clients/{client_id}")
def delete_client(client_id: str, db: Session = Depends(get_db)):
    service = ClientService(db)
    return service.delete_client(client_id) 