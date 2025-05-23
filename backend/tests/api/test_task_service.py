from unittest.mock import MagicMock
import pytest
from service.task_service import get_all_tasks, create_task, update_task_detail, delete_task_detail
from db.models.db_models import Tasks, UserTask, Users
from exceptions import TaskNotFoundException, UserNotFoundException
from datetime import date

@pytest.fixture
def mock_user():
    return Users(
        user_id=1,
        user_name="Megha",
        user_email="megha@gmail.com",
        user_address="Mysore",
        user_phone_no="9977664463",
        password="hashedpassword"  
    )

@pytest.fixture
def mock_task():
    return Tasks(
        task_id = 1,
        task_name = "Studying", 
        task_desc = 'Studying', 
        task_category = 'others'
    )

@pytest.fixture
def mock_user_task():
    return UserTask(
        task_id = 1,
        user_id = 1,
        assigned_date = "",
        due_date = "",
        status = "Pending"
    )

@pytest.fixture
def mock_task_create():
    class MockTaskCreate:
        task_name = "Studying"
        task_desc = "Studying"
        task_category = "others"
        due_date = date.today()
    return MockTaskCreate()

@pytest.fixture
def mock_task_update():
    class MockTaskUpdate:
        task_name = "Studying"
        task_desc = "Studying"
        task_category = "others"
        due_date = date.today()
        status = "Pending"
    return MockTaskUpdate()
()



mock_task_id = 1

@pytest.fixture
def get_mock_session():
    return MagicMock()

def test_get_all_task(get_mock_session):
    get_mock_session.query.return_value.all.return_value = mock_user
    result = get_all_tasks(get_mock_session)
    assert result == mock_user

def test_get_all_task_not_found(get_mock_session):
    get_mock_session.query.return_value.all.return_value = []
    with pytest.raises(TaskNotFoundException):
        get_all_tasks(get_mock_session)


def test_create_task_user_not_found(get_mock_session,mock_task_create,mock_user):

    get_mock_session.query.return_value.filter.return_value.first.return_value = None
    with pytest.raises(UserNotFoundException):
        create_task(mock_task_create, get_mock_session, mock_user.user_email)
    

def test_create_task(get_mock_session,mock_task_create,mock_user):

    get_mock_session.query.return_value.filter.return_value.first.return_value = mock_user
    result = create_task(mock_task_create, get_mock_session, mock_user.user_email)

    assert get_mock_session.add.call_count == 2
    assert get_mock_session.commit.call_count == 2
    assert get_mock_session.refresh.call_count == 1

    assert result == {"message": "Task created and assigned successfully."}    

    

def test_update_task(get_mock_session, mock_task, mock_user_task, mock_task_update):
    get_mock_session.get.return_value = mock_task
    get_mock_session.query.return_value.filter.return_value.first.return_value = mock_user_task
    result = update_task_detail(1, mock_task_update, get_mock_session)
    assert get_mock_session.add.call_count == 2
    assert get_mock_session.commit.call_count == 1
    assert get_mock_session.refresh.call_count == 1

    assert result == {"message": "Task Updated successfully."} 


def test_update_task_not_found(get_mock_session,mock_task_update):
    get_mock_session.get.return_value = None
    get_mock_session.query.return_value.filter.return_value.first.return_value = None
    with pytest.raises(TaskNotFoundException):
        update_task_detail(mock_task_id, mock_task_update, get_mock_session)

def test_delete_task(get_mock_session, mock_task, mock_user_task):
    get_mock_session.get.return_value = mock_task
    get_mock_session.query.return_value.filter.return_value.first.return_value = mock_user_task
    result = delete_task_detail(1, get_mock_session) 
    assert get_mock_session.delete.call_count == 2
    assert get_mock_session.commit.call_count == 1
    assert result == {"message": "Task deleted successfully"}    

def test_delete_task_not_found(get_mock_session):
    get_mock_session.get.return_value = None
    get_mock_session.query.return_value.filter.return_value.first.return_value = None
    with pytest.raises(TaskNotFoundException):
        delete_task_detail(1, get_mock_session)    