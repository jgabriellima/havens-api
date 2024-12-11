import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException

from api_template.api.v1.services.assistant_service import AssistantService
from api_template.api.v1.schemas import assistant_schemas
from api_template.db.models import Assistant

@pytest.fixture
def assistant_service(mock_db_session):
    return AssistantService(mock_db_session)

class TestAssistantService:
    def test_create_assistant(self, assistant_service):
        # Arrange
        assistant_create = assistant_schemas.AssistantCreate(
            name="Test Assistant",
            description="Test Description",
            model="gpt-4",
            instructions="Test Instructions",
            specialization="Test Specialization"
        )
        expected_assistant = Assistant(
            id="123",
            name="Test Assistant",
            description="Test Description",
            model="gpt-4",
            instructions="Test Instructions",
            specialization="Test Specialization"
        )
        assistant_service.db.add = MagicMock()
        assistant_service.db.commit = MagicMock()
        assistant_service.db.refresh = MagicMock()
        
        # Act
        result = assistant_service.create_assistant(assistant_create)
        
        # Assert
        assert result.name == expected_assistant.name
        assert result.description == expected_assistant.description
        assistant_service.db.add.assert_called_once()
        assistant_service.db.commit.assert_called_once()
        assistant_service.db.refresh.assert_called_once()

    def test_get_assistants(self, assistant_service):
        expected_assistants = [
            Assistant(id="1", name="Assistant 1"),
            Assistant(id="2", name="Assistant 2")
        ]
        assistant_service.db.query().offset().limit().all = MagicMock(
            return_value=expected_assistants
        )
        
        result = assistant_service.get_assistants(skip=0, limit=10)
        
        assert result == expected_assistants

    def test_get_assistant_success(self, assistant_service):
        assistant_id = "123"
        expected_assistant = Assistant(id=assistant_id, name="Test Assistant")
        assistant_service.db.query().filter().first = MagicMock(
            return_value=expected_assistant
        )
        
        result = assistant_service.get_assistant(assistant_id)
        
        assert result == expected_assistant

    def test_get_assistant_not_found(self, assistant_service):
        assistant_id = "123"
        assistant_service.db.query().filter().first = MagicMock(return_value=None)
        
        with pytest.raises(HTTPException) as exc_info:
            assistant_service.get_assistant(assistant_id)
        
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Assistant not found"

    def test_associate_assistant_success(self, assistant_service):
        client_id = "123"
        assistant_id = "456"
        assistant_service.get_assistant = MagicMock()
        assistant_service.db.query().filter_by().first = MagicMock(return_value=None)
        assistant_service.db.execute = MagicMock()
        assistant_service.db.commit = MagicMock()
        
        result = assistant_service.associate_assistant(client_id, assistant_id)
        
        assert isinstance(result, assistant_schemas.ClientAssistantAssociation)
        assert result.client_id == client_id
        assert result.assistant_id == assistant_id
        assistant_service.db.execute.assert_called_once()
        assistant_service.db.commit.assert_called_once()

    def test_associate_assistant_already_exists(self, assistant_service):
        client_id = "123"
        assistant_id = "456"
        assistant_service.get_assistant = MagicMock()
        assistant_service.db.query().filter_by().first = MagicMock(
            return_value=True
        )
        
        with pytest.raises(HTTPException) as exc_info:
            assistant_service.associate_assistant(client_id, assistant_id)
        
        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "Association already exists"

    def test_get_client_assistants(self, assistant_service):
        client_id = "123"
        expected_assistants = [
            Assistant(id="1", name="Assistant 1"),
            Assistant(id="2", name="Assistant 2")
        ]
        assistant_service.db.query().join().filter().all = MagicMock(
            return_value=expected_assistants
        )
        
        result = assistant_service.get_client_assistants(client_id)
        
        assert result == expected_assistants

    def test_remove_association_success(self, assistant_service):
        client_id = "123"
        assistant_id = "456"
        assistant_service.db.execute = MagicMock(return_value=MagicMock(rowcount=1))
        assistant_service.db.commit = MagicMock()
        
        result = assistant_service.remove_association(client_id, assistant_id)
        
        assert result == {"status": "success"}
        assistant_service.db.execute.assert_called_once()
        assistant_service.db.commit.assert_called_once()

    def test_remove_association_not_found(self, assistant_service):
        client_id = "123"
        assistant_id = "456"
        assistant_service.db.execute = MagicMock(return_value=MagicMock(rowcount=0))
        
        with pytest.raises(HTTPException) as exc_info:
            assistant_service.remove_association(client_id, assistant_id)
        
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Association not found" 