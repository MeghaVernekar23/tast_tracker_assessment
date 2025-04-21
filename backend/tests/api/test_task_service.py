from unittest.mock import MagicMock
import pytest
from service.task_service import get_all_tasks, create_task, update_task_detail, delete_task_detail
from db.models.db_models import Tasks
from backend.exceptions import TaskNotFoundException

mock_tasks = Tasks(task_id = 1, task_name = "Studying", task_desc = 'Studying', task_category = 'others')

mock_task_create = MagicMock()

mock_task_id = 1

@pytest.fixture
def get_mock_session():
    return MagicMock()

def test_get_all_task(get_mock_session):
    get_mock_session.query.return_value.all.return_value = mock_tasks
    result = get_all_tasks(get_mock_session)
    assert result == mock_tasks

def test_get_all_task_not_found(get_mock_session):
    get_mock_session.query.return_value.all.return_value = []
    with pytest.raises(TaskNotFoundException):
        get_all_tasks(get_mock_session)


def test_create_task(get_mock_session):
    result = create_task(mock_task_create, get_mock_session)
    created_task = get_mock_session.add.call_args[0][0]
    get_mock_session.refresh.assert_called_once_with(created_task)
    assert result.task_name == created_task.task_name        
    assert result.task_desc == created_task.task_desc
    assert result.task_category == created_task.task_category

def test_update_task(get_mock_session):
    get_mock_session.get.return_value = mock_tasks
    result = update_task_detail(mock_task_id, mock_task_create, get_mock_session)
    updated_task = get_mock_session.add.call_args[0][0]
    get_mock_session.refresh.assert_called_once_with(updated_task)
    assert result.task_name == updated_task.task_name        
    assert result.task_desc == updated_task.task_desc
    assert result.task_category == updated_task.task_category


def test_update_task_not_found(get_mock_session):
    get_mock_session.get.return_value = []
    with pytest.raises(TaskNotFoundException):
        update_task_detail(mock_task_id, mock_task_create, get_mock_session)

def test_delete_task(get_mock_session):
    get_mock_session.get.return_value = mock_tasks  
    result = delete_task_detail(mock_task_id, get_mock_session) 
    get_mock_session.delete.assert_called_once_with(mock_tasks)
    get_mock_session.commit.assert_called_once()
    assert result == {"message": "Task deleted successfully"}    

def test_delete_task_not_found(get_mock_session):
    get_mock_session.get.return_value = []
    with pytest.raises(TaskNotFoundException):
        delete_task_detail(mock_task_id, get_mock_session)    