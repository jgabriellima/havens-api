import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException

from api_template.api.v1.services.client_user_service import ClientUserService
from api_template.api.v1.schemas import client_user_schemas

@pytest.fixture
def client_user_service(mock_db_session):
    return ClientUserService(mock_db_session)

class TestClientUserService:
    def test_create_user_success(self, client_user_service):
        # Arrange
        user_create = client_user_schemas.ClientUserCreate(
            email="test@example.com",
            name="Test User"
        )
        expected_user = client_user_schemas.ClientUser(
            id="123",
            email="test@example.com",
            name="Test User"
        )
        client_user_service.repository.get_by_email = MagicMock(return_value=None)
        client_user_service.repository.create = MagicMock(return_value=expected_user)
        
        # Act
        result = client_user_service.create_user(user_create)
        
        # Assert
        assert result == expected_user
        client_user_service.repository.create.assert_called_once_with(user_create)

    def test_create_user_email_already_registered(self, client_user_service):
        user_create = client_user_schemas.ClientUserCreate(
            email="test@example.com",
            name="Test User"
        )
        client_user_service.repository.get_by_email = MagicMock(return_value=True)
        
        with pytest.raises(HTTPException) as exc_info:
            client_user_service.create_user(user_create)
        
        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "Email already registered"

    def test_get_user_success(self, client_user_service):
        user_id = "123"
        expected_user = client_user_schemas.ClientUser(
            id=user_id,
            email="test@example.com",
            name="Test User"
        )
        client_user_service.repository.get_by_id = MagicMock(return_value=expected_user)
        
        result = client_user_service.get_user(user_id)
        
        assert result == expected_user

    def test_get_user_not_found(self, client_user_service):
        user_id = "123"
        client_user_service.repository.get_by_id = MagicMock(return_value=None)
        
        with pytest.raises(HTTPException) as exc_info:
            client_user_service.get_user(user_id)
        
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "User not found"

    def test_get_users_by_client(self, client_user_service):
        client_id = "123"
        expected_users = [
            client_user_schemas.ClientUser(id="1", email="user1@example.com"),
            client_user_schemas.ClientUser(id="2", email="user2@example.com")
        ]
        client_user_service.repository.get_by_client = MagicMock(return_value=expected_users)
        
        result = client_user_service.get_users_by_client(client_id, skip=0, limit=10)
        
        assert result == expected_users

    def test_update_user_success(self, client_user_service):
        user_id = "123"
        user_update = client_user_schemas.ClientUserUpdate(name="Updated User")
        expected_user = client_user_schemas.ClientUser(
            id=user_id,
            email="test@example.com",
            name="Updated User"
        )
        client_user_service.repository.update = MagicMock(return_value=expected_user)
        
        result = client_user_service.update_user(user_id, user_update)
        
        assert result == expected_user

    def test_update_user_not_found(self, client_user_service):
        user_id = "123"
        user_update = client_user_schemas.ClientUserUpdate(name="Updated User")
        client_user_service.repository.update = MagicMock(return_value=None)
        
        with pytest.raises(HTTPException) as exc_info:
            client_user_service.update_user(user_id, user_update)
        
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "User not found"

    def test_delete_user_success(self, client_user_service):
        user_id = "123"
        client_user_service.repository.delete = MagicMock(return_value=True)
        
        result = client_user_service.delete_user(user_id)
        
        assert result is True

    def test_delete_user_not_found(self, client_user_service):
        user_id = "123"
        client_user_service.repository.delete = MagicMock(return_value=False)
        
        with pytest.raises(HTTPException) as exc_info:
            client_user_service.delete_user(user_id)
        
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "User not found" 