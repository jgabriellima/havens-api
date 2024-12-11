from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
import enum

from api_template.db.base import Base

class TaskStatus(enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class BackgroundTask(Base):
    __tablename__ = "background_tasks"

    id = Column(String(36), primary_key=True)
    session_id = Column(String(36), ForeignKey("sessions.id"), nullable=True)
    task_type = Column(String, nullable=False)  # String livre para suportar qualquer tipo de tarefa
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING)
    result_data = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    session = relationship("Session", back_populates="tasks")
    events = relationship("Event", back_populates="task")
