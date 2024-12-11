import pytest
from unittest.mock import Mock, MagicMock
from fastapi import HTTPException

from api_template.api.v1.services.task_service import TaskService
from api_template.api.v1.schemas import task_schemas

@pytest.fixture
def task_service(mock_db_session):
    return TaskService(mock_db_session)

class TestTaskService:
    def test_create_task(self, task_service):
        # Arrange
        task_create = task_schemas.TaskCreate(name="Test Task")
        expected_task = task_schemas.Task(id="123", name="Test Task")
        task_service.repository.create = MagicMock(return_value=expected_task)
        
        # Act
        result = task_service.create_task(task_create)
        
        # Assert
        assert result == expected_task
        task_service.repository.create.assert_called_once_with(task_create)

    def test_get_task_success(self, task_service):
        task_id = "123"
        expected_task = task_schemas.Task(id=task_id, name="Test Task")
        task_service.repository.get_by_id = MagicMock(return_value=expected_task)
        
        result = task_service.get_task(task_id)
        
        assert result == expected_task
        task_service.repository.get_by_id.assert_called_once_with(task_id)

    def test_get_task_not_found(self, task_service):
        task_id = "123"
        task_service.repository.get_by_id = MagicMock(return_value=None)
        
        with pytest.raises(HTTPException) as exc_info:
            task_service.get_task(task_id)
        
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Task not found"

    def test_get_tasks(self, task_service):
        expected_tasks = [
            task_schemas.Task(id="1", name="Task 1"),
            task_schemas.Task(id="2", name="Task 2")
        ]
        task_service.repository.get_all = MagicMock(return_value=expected_tasks)
        
        result = task_service.get_tasks(skip=0, limit=10)
        
        assert result == expected_tasks
        task_service.repository.get_all.assert_called_once_with(skip=0, limit=10)

    def test_get_session_tasks(self, task_service):
        session_id = "123"
        expected_tasks = [
            task_schemas.Task(id="1", name="Task 1"),
            task_schemas.Task(id="2", name="Task 2")
        ]
        task_service.repository.get_by_session = MagicMock(return_value=expected_tasks)
        
        result = task_service.get_session_tasks(session_id, skip=0, limit=10)
        
        assert result == expected_tasks
        task_service.repository.get_by_session.assert_called_once_with(session_id, skip=0, limit=10)

    def test_update_task_success(self, task_service):
        task_id = "123"
        task_update = task_schemas.TaskUpdate(name="Updated Task")
        expected_task = task_schemas.Task(id=task_id, name="Updated Task")
        task_service.repository.update = MagicMock(return_value=expected_task)
        
        result = task_service.update_task(task_id, task_update)
        
        assert result == expected_task
        task_service.repository.update.assert_called_once_with(task_id, task_update)

    def test_update_task_not_found(self, task_service):
        task_id = "123"
        task_update = task_schemas.TaskUpdate(name="Updated Task")
        task_service.repository.update = MagicMock(return_value=None)
        
        with pytest.raises(HTTPException) as exc_info:
            task_service.update_task(task_id, task_update)
        
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Task not found"

    def test_delete_task_success(self, task_service):
        task_id = "123"
        task_service.repository.delete = MagicMock(return_value=True)
        
        result = task_service.delete_task(task_id)
        
        assert result is True
        task_service.repository.delete.assert_called_once_with(task_id)

    def test_delete_task_not_found(self, task_service):
        task_id = "123"
        task_service.repository.delete = MagicMock(return_value=False)
        
        with pytest.raises(HTTPException) as exc_info:
            task_service.delete_task(task_id)
        
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Task not found" 