from typing import List, Optional
from sqlalchemy.orm import Session
from uuid import uuid4
from datetime import datetime

from api_template.db.models.call import Call
from api_template.api.v1.schemas import call_schemas

class CallRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, call: call_schemas.CallCreate) -> Call:
        db_call = Call(
            id=str(uuid4()),
            session_id=call.session_id,
            direction=call.direction,
            sip_trunk_id=call.sip_trunk_id,
            status=call_schemas.CallStatus.INITIATED,
            start_time=datetime.utcnow()
        )
        self.db_session.add(db_call)
        self.db_session.commit()
        self.db_session.refresh(db_call)
        return db_call

    def get_by_id(self, call_id: str) -> Optional[Call]:
        return self.db_session.query(Call)\
            .filter(Call.id == call_id).first()

    def get_by_session(self, session_id: str, skip: int = 0, limit: int = 100) -> List[Call]:
        return self.db_session.query(Call)\
            .filter(Call.session_id == session_id)\
            .order_by(Call.start_time.desc())\
            .offset(skip).limit(limit).all()

    def update_status(self, call_id: str, status: call_schemas.CallStatus) -> Optional[Call]:
        db_call = self.get_by_id(call_id)
        if db_call:
            db_call.status = status
            if status == call_schemas.CallStatus.COMPLETED:
                db_call.end_time = datetime.utcnow()
            self.db_session.commit()
            self.db_session.refresh(db_call)
        return db_call 