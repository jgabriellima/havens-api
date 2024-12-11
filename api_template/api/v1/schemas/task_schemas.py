from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class TaskBase(BaseModel):
    function_name: str
    agent_id: int
    description: Optional[str] = None
    retry: Optional[bool] = True
    input_data: Optional[str] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    status: str
    output_data: Optional[str] = None
    retry: Optional[bool] = None

class Task(TaskBase):
    id: int
    task_id: str
    status: str
    output_data: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True 