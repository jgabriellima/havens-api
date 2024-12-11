import pytest
from unittest.mock import MagicMock
from uuid import UUID

from api_template.api.v1.services.event_service import EventService
from api_template.api.v1.schemas import event_schemas
from api_template.db.models.event import Event

@pytest.fixture
def event_service(mock_db_session):
    return EventService(mock_db_session)

class TestEventService:
    def test_get_session_events(self, event_service):
        # Arrange
        session_id = "123"
        expected_events = [
            Event(id="1", type="system", description="Event 1"),
            Event(id="2", type="system", description="Event 2")
        ]
        event_service.db.query().filter().offset().limit().all = MagicMock(
            return_value=expected_events
        )
        
        # Act
        result = event_service.get_session_events(session_id, skip=0, limit=10)
        
        # Assert
        assert result == expected_events

    def test_get_client_events(self, event_service):
        client_id = "123"
        expected_events = [
            Event(id="1", type="system", description="Event 1"),
            Event(id="2", type="system", description="Event 2")
        ]
        event_service.db.query().filter().offset().limit().all = MagicMock(
            return_value=expected_events
        )
        
        result = event_service.get_client_events(client_id, skip=0, limit=10)
        
        assert result == expected_events

    def test_create_system_event(self, event_service):
        event_create = event_schemas.SystemEventCreate(
            description="Test System Event",
            metadata={"key": "value"}
        )
        event_service.db.add = MagicMock()
        event_service.db.commit = MagicMock()
        event_service.db.refresh = MagicMock()
        
        result = event_service.create_system_event(event_create)
        
        assert isinstance(result, Event)
        assert result.type == "system"
        assert result.description == "Test System Event"
        assert result.metadata == {"key": "value"}
        event_service.db.add.assert_called_once()
        event_service.db.commit.assert_called_once()

    def test_create_task_event(self, event_service):
        event_create = event_schemas.TaskEventCreate(
            description="Test Task Event",
            task_id="123",
            metadata={"key": "value"}
        )
        event_service.db.add = MagicMock()
        event_service.db.commit = MagicMock()
        event_service.db.refresh = MagicMock()
        
        result = event_service.create_task_event(event_create)
        
        assert isinstance(result, Event)
        assert result.type == "task"
        assert result.description == "Test Task Event"
        assert result.task_id == "123"
        assert result.metadata == {"key": "value"}
        event_service.db.add.assert_called_once()
        event_service.db.commit.assert_called_once()

    def test_create_session_event(self, event_service):
        event_create = event_schemas.SessionEventCreate(
            description="Test Session Event",
            session_id="123",
            metadata={"key": "value"}
        )
        event_service.db.add = MagicMock()
        event_service.db.commit = MagicMock()
        event_service.db.refresh = MagicMock()
        
        result = event_service.create_session_event(event_create)
        
        assert isinstance(result, Event)
        assert result.type == "session"
        assert result.description == "Test Session Event"
        assert result.session_id == "123"
        assert result.metadata == {"key": "value"}
        event_service.db.add.assert_called_once()
        event_service.db.commit.assert_called_once()

    def test_get_event(self, event_service):
        event_id = "123"
        expected_event = Event(
            id=event_id,
            type="system",
            description="Test Event"
        )
        event_service.db.query().filter().first = MagicMock(return_value=expected_event)
        
        result = event_service.get_event(event_id)
        
        assert result == expected_event 