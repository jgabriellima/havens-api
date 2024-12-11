import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException

from api_template.api.v1.services.message_service import MessageService
from api_template.api.v1.schemas import message_schemas
from api_template.db.models.session import Session as SessionModel

@pytest.fixture
def message_service(mock_db_session):
    return MessageService(mock_db_session)

class TestMessageService:
    async def test_create_message_success(self, message_service, mock_background_tasks):
        # Arrange
        session_id = "123"
        message_create = message_schemas.MessageCreate(
            content="Test message",
            content_type=message_schemas.ContentType.TEXT
        )
        session = MagicMock(spec=SessionModel)
        session.end_time = None
        expected_message = message_schemas.Message(
            id="1",
            session_id=session_id,
            content="Test message",
            content_type=message_schemas.ContentType.TEXT
        )
        
        message_service.session_repository.get_by_id = MagicMock(return_value=session)
        message_service.repository.create = MagicMock(return_value=expected_message)
        
        # Act
        result = await message_service.create_message(
            session_id,
            message_create,
            mock_background_tasks
        )
        
        # Assert
        assert result == expected_message
        message_service.repository.create.assert_called_once_with(session_id, message_create)

    async def test_create_message_session_not_found(self, message_service, mock_background_tasks):
        session_id = "123"
        message_create = message_schemas.MessageCreate(
            content="Test message",
            content_type=message_schemas.ContentType.TEXT
        )
        
        message_service.session_repository.get_by_id = MagicMock(return_value=None)
        
        with pytest.raises(HTTPException) as exc_info:
            await message_service.create_message(
                session_id,
                message_create,
                mock_background_tasks
            )
        
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Session not found"

    async def test_create_message_session_ended(self, message_service, mock_background_tasks):
        session_id = "123"
        message_create = message_schemas.MessageCreate(
            content="Test message",
            content_type=message_schemas.ContentType.TEXT
        )
        session = MagicMock(spec=SessionModel)
        session.end_time = "2023-01-01T00:00:00"
        
        message_service.session_repository.get_by_id = MagicMock(return_value=session)
        
        with pytest.raises(HTTPException) as exc_info:
            await message_service.create_message(
                session_id,
                message_create,
                mock_background_tasks
            )
        
        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "Session already ended"

    def test_get_session_messages(self, message_service):
        session_id = "123"
        expected_messages = [
            message_schemas.Message(
                id="1",
                session_id=session_id,
                content="Message 1",
                content_type=message_schemas.ContentType.TEXT
            ),
            message_schemas.Message(
                id="2",
                session_id=session_id,
                content="Message 2",
                content_type=message_schemas.ContentType.TEXT
            )
        ]
        
        message_service.repository.get_by_session = MagicMock(return_value=expected_messages)
        
        result = message_service.get_session_messages(session_id, skip=0, limit=10)
        
        assert result == expected_messages
        message_service.repository.get_by_session.assert_called_once_with(
            session_id,
            skip=0,
            limit=10
        ) 