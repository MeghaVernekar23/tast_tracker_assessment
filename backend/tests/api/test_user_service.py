
from turtle import update
import pytest
from service.user_service import get_all_user, get_user_by_id, get_user_by_username,create_user, update_user_details, delete_user_detail
from db.models.db_models import Users
from unittest.mock import MagicMock
from backend.exceptions import UserNotFoundException
from db.models.pydantic_models import UserCreatePydantic

mock_users = Users(user_id = 1,user_name = "Megha", user_address = "Mysore", user_phone_no = "9977664463")
mock_user_create = MagicMock()
mock_user_id = 1
mock_user_name = "Megha"

@pytest.fixture
def get_mock_session():
    return MagicMock()

def test_get_all_user(get_mock_session):
    get_mock_session.query.return_value.all.return_value = mock_users
    result = get_all_user(get_mock_session)
    assert result == mock_users

def test_get_all_user_not_fount(get_mock_session):
    get_mock_session.query.return_value.all.return_value = []
    with pytest.raises(UserNotFoundException):
        get_all_user(get_mock_session)


def test_get_user_by_id(get_mock_session):
    get_mock_session.get.return_value = mock_users
    result = get_user_by_id(mock_user_id,get_mock_session)
    assert result == mock_users


def test_get_user_by_id_not_found(get_mock_session):
    get_mock_session.get.return_value = []
    with pytest.raises(UserNotFoundException):
        get_user_by_id(2, get_mock_session)


def test_get_user_by_username(get_mock_session):
    get_mock_session.query.return_value.filter.return_value.all.return_value = mock_users
    result = get_user_by_username(mock_user_name, get_mock_session)
    assert result == mock_users

def test_get_user_by_username_not_found(get_mock_session):
    get_mock_session.query.return_value.filter.return_value.all.return_value = []
    with pytest.raises(UserNotFoundException):
        get_user_by_username(mock_user_name, get_mock_session)    

def test_create_user(get_mock_session):
    result = create_user(mock_user_create, get_mock_session)
    created_user = get_mock_session.add.call_args[0][0]
    get_mock_session.refresh.assert_called_once_with(created_user)
    assert result.user_name == created_user.user_name        
    assert result.user_address == created_user.user_address
    assert result.user_phone_no == created_user.user_phone_no

def test_update_user(get_mock_session):
    get_mock_session.get.return_value = mock_users
    result = update_user_details(mock_user_id, mock_user_create, get_mock_session)
    updated_user = get_mock_session.add.call_args[0][0]
    get_mock_session.refresh.assert_called_once_with(updated_user)
    assert result.user_name == updated_user.user_name        
    assert result.user_address == updated_user.user_address
    assert result.user_phone_no == updated_user.user_phone_no

def test_update_user_not_found(get_mock_session):
    get_mock_session.get.return_value = []
    with pytest.raises(UserNotFoundException):
        update_user_details(mock_user_id, mock_user_create, get_mock_session)
    
def test_delete_user(get_mock_session):
    get_mock_session.get.return_value = mock_users
    result = delete_user_detail(mock_user_id, get_mock_session)   
    get_mock_session.delete.assert_called_once_with(mock_users)
    get_mock_session.commit.assert_called_once()
    assert result == {"message": "User deleted successfully"}

def test_delete_user_not_found(get_mock_session):
    get_mock_session.get.return_value = []
    with pytest.raises(UserNotFoundException):
        delete_user_detail(mock_user_id, get_mock_session)    