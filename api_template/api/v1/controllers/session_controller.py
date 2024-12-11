from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/sessions/", response_model=session_schemas.Session)
def create_session(session: session_schemas.SessionCreate, db: Session = Depends(get_db)):
    service = SessionService(db)
    return service.create_session(session)

@router.get("/clients/{client_id}/sessions/active", response_model=List[session_schemas.Session])
def list_active_sessions(client_id: str, db: Session = Depends(get_db)):
    service = SessionService(db)
    return service.get_active_sessions(client_id)

@router.post("/sessions/{session_id}/end", response_model=session_schemas.Session)
def end_session(session_id: str, db: Session = Depends(get_db)):
    service = SessionService(db)
    return service.end_session(session_id) 