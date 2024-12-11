import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from datetime import datetime

from api_template.api.v1.services.call_service import CallService
from api_template.api.v1.schemas import call_schemas

@pytest.fixture
def call_service(mock_db_session):
    return CallService(mock_db_session)

class TestCallService:
    @pytest.mark.asyncio
    async def test_initiate_call_success(self, call_service, mock_background_tasks):
        # Arrange
        call_create = call_schemas.CallCreate(
            direction=call_schemas.CallDirection.OUTBOUND,
            phone_number="+1234567890"
        )
        expected_call = call_schemas.Call(
            id="123",
            direction=call_schemas.CallDirection.OUTBOUND,
            phone_number="+1234567890",
            status=call_schemas.CallStatus.INITIATED
        )
        call_service.repository.create = MagicMock(return_value=expected_call)
        
        # Act
        async def test_initiate_call():
            result = await call_service.initiate_call(call_create, mock_background_tasks)
            assert result == expected_call
            call_service.repository.create.assert_called_once_with(call_create)
        
        # Assert
        await test_initiate_call()

    async def test_initiate_call_invalid_direction(self, call_service, mock_background_tasks):
        call_create = call_schemas.CallCreate(
            direction=call_schemas.CallDirection.INBOUND,
            phone_number="+1234567890"
        )
        
        with pytest.raises(HTTPException) as exc_info:
            await call_service.initiate_call(call_create, mock_background_tasks)
        
        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "Only outbound calls can be initiated through this endpoint"

    def test_get_session_calls(self, call_service):
        session_id = "123"
        current_time = datetime.utcnow()
        expected_calls = [
            call_schemas.Call(
                id="1",
                session_id=session_id,
                direction=call_schemas.CallDirection.OUTBOUND,
                status=call_schemas.CallStatus.COMPLETED,
                start_time=current_time,
                end_time=current_time
            ),
            call_schemas.Call(
                id="2",
                session_id=session_id,
                direction=call_schemas.CallDirection.INBOUND,
                status=call_schemas.CallStatus.COMPLETED,
                start_time=current_time,
                end_time=current_time
            )
        ]
        call_service.repository.get_by_session = MagicMock(return_value=expected_calls)
        
        result = call_service.get_session_calls(session_id, skip=0, limit=10)
        
        assert result == expected_calls
        call_service.repository.get_by_session.assert_called_once_with(session_id, 0, 10)

    async def test_end_call_success(self, call_service):
        call_id = "123"
        expected_call = call_schemas.Call(
            id=call_id,
            status=call_schemas.CallStatus.COMPLETED
        )
        call_service.repository.update_status = MagicMock(return_value=expected_call)
        
        result = await call_service.end_call(call_id)
        
        assert result == expected_call
        call_service.repository.update_status.assert_called_once_with(
            call_id,
            call_schemas.CallStatus.COMPLETED
        )

    async def test_end_call_not_found(self, call_service):
        call_id = "123"
        call_service.repository.update_status = MagicMock(return_value=None)
        
        with pytest.raises(HTTPException) as exc_info:
            await call_service.end_call(call_id)
        
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Call not found"

    def test_get_call_status_success(self, call_service):
        call_id = "123"
        current_time = datetime.utcnow()
        expected_call = call_schemas.Call(
            id=call_id,
            session_id="session_123",
            direction=call_schemas.CallDirection.OUTBOUND,
            status=call_schemas.CallStatus.IN_PROGRESS,
            start_time=current_time,
            end_time=None
        )
        call_service.repository.get_by_id = MagicMock(return_value=expected_call)
        
        result = call_service.get_call_status(call_id)
        
        assert result == call_schemas.CallStatus.IN_PROGRESS

    def test_get_call_status_not_found(self, call_service):
        call_id = "123"
        call_service.repository.get_by_id = MagicMock(return_value=None)
        
        with pytest.raises(HTTPException) as exc_info:
            call_service.get_call_status(call_id)
        
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Call not found" 