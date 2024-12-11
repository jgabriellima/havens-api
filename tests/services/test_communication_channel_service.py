import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException

from api_template.api.v1.services.communication_channel_service import CommunicationChannelService
from api_template.api.v1.schemas import communication_channel_schemas

@pytest.fixture
def communication_channel_service(mock_db_session):
    return CommunicationChannelService(mock_db_session)

class TestCommunicationChannelService:
    def test_create_channel_success(self, communication_channel_service):
        # Arrange
        channel_create = communication_channel_schemas.CommunicationChannelCreate(
            channel_identifier="test_channel"
        )
        expected_channel = communication_channel_schemas.CommunicationChannel(
            id="123",
            channel_identifier="test_channel"
        )
        communication_channel_service.repository.get_by_identifier = MagicMock(return_value=None)
        communication_channel_service.repository.create = MagicMock(return_value=expected_channel)
        
        # Act
        result = communication_channel_service.create_channel(channel_create)
        
        # Assert
        assert result == expected_channel
        communication_channel_service.repository.create.assert_called_once_with(channel_create)

    def test_create_channel_identifier_already_registered(self, communication_channel_service):
        channel_create = communication_channel_schemas.CommunicationChannelCreate(
            channel_identifier="test_channel"
        )
        communication_channel_service.repository.get_by_identifier = MagicMock(return_value=True)
        
        with pytest.raises(HTTPException) as exc_info:
            communication_channel_service.create_channel(channel_create)
        
        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "Channel identifier already registered"

    def test_get_channel_success(self, communication_channel_service):
        channel_id = "123"
        expected_channel = communication_channel_schemas.CommunicationChannel(
            id=channel_id,
            channel_identifier="test_channel"
        )
        communication_channel_service.repository.get_by_id = MagicMock(return_value=expected_channel)
        
        result = communication_channel_service.get_channel(channel_id)
        
        assert result == expected_channel

    def test_get_channel_not_found(self, communication_channel_service):
        channel_id = "123"
        communication_channel_service.repository.get_by_id = MagicMock(return_value=None)
        
        with pytest.raises(HTTPException) as exc_info:
            communication_channel_service.get_channel(channel_id)
        
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Channel not found"

    def test_get_channels_by_client(self, communication_channel_service):
        client_id = "123"
        expected_channels = [
            communication_channel_schemas.CommunicationChannel(id="1", channel_identifier="channel1"),
            communication_channel_schemas.CommunicationChannel(id="2", channel_identifier="channel2")
        ]
        communication_channel_service.repository.get_by_client = MagicMock(return_value=expected_channels)
        
        result = communication_channel_service.get_channels_by_client(client_id, skip=0, limit=10)
        
        assert result == expected_channels

    def test_update_channel_success(self, communication_channel_service):
        channel_id = "123"
        channel_update = communication_channel_schemas.CommunicationChannelUpdate(channel_identifier="updated_channel")
        expected_channel = communication_channel_schemas.CommunicationChannel(
            id=channel_id,
            channel_identifier="updated_channel"
        )
        communication_channel_service.repository.update = MagicMock(return_value=expected_channel)
        
        result = communication_channel_service.update_channel(channel_id, channel_update)
        
        assert result == expected_channel

    def test_update_channel_not_found(self, communication_channel_service):
        channel_id = "123"
        channel_update = communication_channel_schemas.CommunicationChannelUpdate(channel_identifier="updated_channel")
        communication_channel_service.repository.update = MagicMock(return_value=None)
        
        with pytest.raises(HTTPException) as exc_info:
            communication_channel_service.update_channel(channel_id, channel_update)
        
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Channel not found"

    def test_delete_channel_success(self, communication_channel_service):
        channel_id = "123"
        communication_channel_service.repository.delete = MagicMock(return_value=True)
        
        result = communication_channel_service.delete_channel(channel_id)
        
        assert result is True

    def test_delete_channel_not_found(self, communication_channel_service):
        channel_id = "123"
        communication_channel_service.repository.delete = MagicMock(return_value=False)
        
        with pytest.raises(HTTPException) as exc_info:
            communication_channel_service.delete_channel(channel_id)
        
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Channel not found" 