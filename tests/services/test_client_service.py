import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from datetime import datetime

from api_template.api.v1.services.client_service import ClientService
from api_template.api.v1.schemas import client_schemas

@pytest.fixture
def client_service(mock_db_session):
    return ClientService(mock_db_session)

class TestClientService:
    def test_create_client(self, client_service):
        # Arrange
        current_time = datetime.utcnow()
        client_create = client_schemas.ClientCreate(
            name="Test Client",
            additional_info={"description": "Test Description"}
        )
        expected_client = client_schemas.Client(
            id="123",
            name="Test Client",
            additional_info={"description": "Test Description"},
            created_at=current_time,
            updated_at=current_time
        )
        client_service.repository.create = MagicMock(return_value=expected_client)
        
        # Act
        result = client_service.create_client(client_create)
        
        # Assert
        assert result == expected_client
        client_service.repository.create.assert_called_once_with(client_create)

    def test_get_client_success(self, client_service):
        current_time = datetime.utcnow()
        client_id = "123"
        expected_client = client_schemas.Client(
            id=client_id,
            name="Test Client",
            additional_info={"description": "Test Description"},
            created_at=current_time,
            updated_at=current_time
        )
        client_service.repository.get_by_id = MagicMock(return_value=expected_client)
        
        result = client_service.get_client(client_id)
        
        assert result == expected_client
        client_service.repository.get_by_id.assert_called_once_with(client_id)

    def test_get_client_not_found(self, client_service):
        client_id = "123"
        client_service.repository.get_by_id = MagicMock(return_value=None)
        
        with pytest.raises(HTTPException) as exc_info:
            client_service.get_client(client_id)
        
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Client not found"

    def test_get_clients(self, client_service):
        current_time = datetime.utcnow()
        expected_clients = [
            client_schemas.Client(
                id="1",
                name="Client 1",
                created_at=current_time,
                updated_at=current_time
            ),
            client_schemas.Client(
                id="2",
                name="Client 2",
                created_at=current_time,
                updated_at=current_time
            )
        ]
        client_service.repository.get_all = MagicMock(return_value=expected_clients)
        
        result = client_service.get_clients(skip=0, limit=10)
        
        assert result == expected_clients
        client_service.repository.get_all.assert_called_once_with(skip=0, limit=10)

    def test_update_client_success(self, client_service):
        client_id = "123"
        client_update = client_schemas.ClientUpdate(name="Updated Client")
        expected_client = client_schemas.Client(
            id=client_id,
            name="Updated Client"
        )
        client_service.repository.update = MagicMock(return_value=expected_client)
        
        result = client_service.update_client(client_id, client_update)
        
        assert result == expected_client
        client_service.repository.update.assert_called_once_with(client_id, client_update)

    def test_update_client_not_found(self, client_service):
        client_id = "123"
        client_update = client_schemas.ClientUpdate(name="Updated Client")
        client_service.repository.update = MagicMock(return_value=None)
        
        with pytest.raises(HTTPException) as exc_info:
            client_service.update_client(client_id, client_update)
        
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Client not found"

    def test_delete_client_success(self, client_service):
        client_id = "123"
        client_service.repository.delete = MagicMock(return_value=True)
        
        result = client_service.delete_client(client_id)
        
        assert result is True
        client_service.repository.delete.assert_called_once_with(client_id)

    def test_delete_client_not_found(self, client_service):
        client_id = "123"
        client_service.repository.delete = MagicMock(return_value=False)
        
        with pytest.raises(HTTPException) as exc_info:
            client_service.delete_client(client_id)
        
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Client not found" 