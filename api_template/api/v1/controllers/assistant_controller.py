from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api_template.api.v1.schemas import assistant_schemas
from api_template.api.v1.services.assistant_service import AssistantService
from api_template.db.session import get_db

router = APIRouter()

@router.post("/assistants/", response_model=assistant_schemas.Assistant)
def create_assistant(
    assistant: assistant_schemas.AssistantCreate,
    db: Session = Depends(get_db)
):
    service = AssistantService(db)
    return service.create_assistant(assistant)

@router.get("/assistants/", response_model=List[assistant_schemas.Assistant])
def list_assistants(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    service = AssistantService(db)
    return service.get_assistants(skip=skip, limit=limit)

@router.post("/clients/{client_id}/assistants/{assistant_id}", response_model=assistant_schemas.ClientAssistant)
def associate_assistant(
    client_id: str,
    assistant_id: str,
    db: Session = Depends(get_db)
):
    service = AssistantService(db)
    return service.associate_assistant(client_id, assistant_id)

@router.get("/clients/{client_id}/assistants/", response_model=List[assistant_schemas.Assistant])
def list_client_assistants(
    client_id: str,
    db: Session = Depends(get_db)
):
    service = AssistantService(db)
    return service.get_client_assistants(client_id)

@router.delete("/clients/{client_id}/assistants/{assistant_id}")
def remove_assistant_association(
    client_id: str,
    assistant_id: str,
    db: Session = Depends(get_db)
):
    service = AssistantService(db)
    return service.remove_association(client_id, assistant_id) 