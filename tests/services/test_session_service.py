import pytest
from unittest.mock import Mock, MagicMock, AsyncMock
from datetime import datetime
from fastapi import HTTPException

from api_template.api.v1.services.session_service import SessionService
from api_template.api.v1.schemas import session_schemas

@pytest.fixture
def session_service(mock_db_session):
    return SessionService(mock_db_session)

class TestSessionService:
    def test_create_session_success(self, session_service):
        # Arrange
        session_create = session_schemas.SessionCreate(
            client_id="123",
            end_user_id="456"
        )
        expected_session = session_schemas.Session(
            id="789",
            client_id="123",
            end_user_id="456"
        )
        session_service.repository.get_active_by_client = MagicMock(return_value=[])
        session_service.repository.create = MagicMock(return_value=expected_session)
        
        # Act
        result = session_service.create_session(session_create)
        
        # Assert
        assert result == expected_session
        session_service.repository.create.assert_called_once_with(session_create)

    def test_create_session_with_active_session(self, session_service):
        session_create = session_schemas.SessionCreate(
            client_id="123",
            end_user_id="456"
        )
        active_session = session_schemas.Session(
            id="789",
            client_id="123",
            end_user_id="456"
        )
        session_service.repository.get_active_by_client = MagicMock(return_value=[active_session])
        session_service.repository.end_session = MagicMock()
        session_service.repository.create = MagicMock()
        
        session_service.create_session(session_create)
        
        session_service.repository.end_session.assert_called_once_with(active_session.id)

    def test_get_session_success(self, session_service):
        session_id = "123"
        expected_session = session_schemas.Session(
            id=session_id,
            client_id="456"
        )
        session_service.repository.get_by_id = MagicMock(return_value=expected_session)
        
        result = session_service.get_session(session_id)
        
        assert result == expected_session

    async def test_get_session_not_found(self, session_service):
        # Configure o mock
        mock_session = MagicMock()
        mock_session.query.return_value.filter.return_value.first.return_value = None
        
        # Teste
        result = await session_service.get_session("non_existent_id")
        assert result is None

    def test_get_active_sessions(self, session_service):
        client_id = "123"
        expected_sessions = [
            session_schemas.Session(id="1", client_id=client_id),
            session_schemas.Session(id="2", client_id=client_id)
        ]
        session_service.repository.get_active_by_client = MagicMock(return_value=expected_sessions)
        
        result = session_service.get_active_sessions(client_id)
        
        assert result == expected_sessions

    def test_get_sessions_by_client(self, session_service):
        client_id = "123"
        expected_sessions = [
            session_schemas.Session(id="1", client_id=client_id),
            session_schemas.Session(id="2", client_id=client_id)
        ]
        session_service.repository.get_by_client = MagicMock(return_value=expected_sessions)
        
        result = session_service.get_sessions_by_client(client_id, skip=0, limit=10)
        
        assert result == expected_sessions

    def test_end_session_success(self, session_service):
        session_id = "123"
        expected_session = session_schemas.Session(
            id=session_id,
            client_id="456"
        )
        session_service.repository.end_session = MagicMock(return_value=expected_session)
        
        result = session_service.end_session(session_id)
        
        assert result == expected_session

    async def test_end_session_not_found(self, session_service):
        # Configure o mock
        mock_session = MagicMock()
        mock_session.query.return_value.filter.return_value.first.return_value = None
        
        # Teste
        result = await session_service.end_session("non_existent_id")
        assert result is None

    def test_update_session_success(self, session_service):
        session_id = "123"
        session_update = session_schemas.SessionUpdate(
            end_user_id="789"
        )
        expected_session = session_schemas.Session(
            id=session_id,
            client_id="456",
            end_user_id="789"
        )
        session_service.repository.update = MagicMock(return_value=expected_session)
        
        result = session_service.update_session(session_id, session_update)
        
        assert result == expected_session

    def test_update_session_not_found(self, session_service):
        session_id = "123"
        session_update = session_schemas.SessionUpdate(
            end_user_id="789"
        )
        session_service.repository.update = MagicMock(return_value=None)
        
        with pytest.raises(HTTPException) as exc_info:
            session_service.update_session(session_id, session_update)
        
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Session not found" 

    async def test_create_session_success(self, session_service):
        session_data = session_schemas.SessionCreate(
            client_id="123",
            end_user_id="456",
            channel_id="channel_1",
            user_id="user_1",
            assistant_id="assistant_1",
            livekit_room_id="room_1"
        )
        
        # Configure o mock para retornar um objeto Session válido
        mock_session = session_schemas.Session(
            id="new_session_id",
            client_id=session_data.client_id,
            end_user_id=session_data.end_user_id,
            channel_id=session_data.channel_id,
            user_id=session_data.user_id,
            assistant_id=session_data.assistant_id,
            livekit_room_id=session_data.livekit_room_id,
            start_time=datetime.now(),
            end_time=None
        )
        
        # Configure o mock do db_session
        session_service.db_session.add = AsyncMock()
        session_service.db_session.commit = AsyncMock()
        session_service.db_session.refresh = AsyncMock()
        
        result = await session_service.create_session(session_data)
        assert result is not None
        assert result.client_id == session_data.client_id 