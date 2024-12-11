from typing import List, Optional
from fastapi import HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from api_template.api.v1.schemas import call_schemas
from api_template.api.v1.repositories.call_repository import CallRepository

class CallService:
    def __init__(self, db: Session):
        self.repository = CallRepository(db)

    async def initiate_call(
        self, 
        call: call_schemas.CallCreate, 
        background_tasks: BackgroundTasks
    ) -> call_schemas.Call:
        # Validar se a direção é outbound
        if call.direction != call_schemas.CallDirection.OUTBOUND:
            raise HTTPException(
                status_code=400,
                detail="Only outbound calls can be initiated through this endpoint"
            )
        
        # Criar a chamada no banco
        db_call = self.repository.create(call)
        
        # Aqui você pode adicionar tarefas em background se necessário
        # Por exemplo, integração com um serviço de telefonia
        # background_tasks.add_task(self._start_outbound_call, db_call.id)
        
        return db_call

    def get_session_calls(
        self, 
        session_id: str, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[call_schemas.Call]:
        return self.repository.get_by_session(session_id, skip, limit)

    async def end_call(self, call_id: str) -> call_schemas.Call:
        call = self.repository.update_status(
            call_id, 
            call_schemas.CallStatus.COMPLETED
        )
        if not call:
            raise HTTPException(
                status_code=404,
                detail="Call not found"
            )
        return call

    def get_call_status(self, call_id: str) -> call_schemas.CallStatus:
        call = self.repository.get_by_id(call_id)
        if not call:
            raise HTTPException(
                status_code=404,
                detail="Call not found"
            )
        return call.status 