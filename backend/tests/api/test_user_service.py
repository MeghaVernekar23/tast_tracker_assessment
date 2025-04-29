
from turtle import update
from unittest.mock import patch
import pytest
from backend.db.models.pydantic_models import UserCreatePydantic
from service.user_service import get_all_user,create_user, update_user_details, delete_user_detail, get_user_by_user_email
from db.models.db_models import Users
from unittest.mock import MagicMock
from exceptions import UserNotFoundException, InvalidCredentialException, UserAlreadyExistsException
from fastapi.security import OAuth2PasswordRequestForm


mock_user_create = MagicMock()
mock_user_id = 1
mock_user_name = "Megha"

@pytest.fixture
def get_mock_session():
    return MagicMock()

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
def mock_create_user():
    return UserCreatePydantic(
        user_id=1,
        user_name="Megha",
        user_email="megha@gmail.com",
        user_address="Mysore",
        user_phone_no="9977664463",
        user_password="dummypassword"  
    )

@pytest.fixture
def mock_login_form():
    form = MagicMock(spec=OAuth2PasswordRequestForm)
    form.username = "megha@gmail.com"
    form.password = "correctpassword"
    return form



def test_get_all_user(get_mock_session):
    get_mock_session.query.return_value.all.return_value = mock_user
    result = get_all_user(get_mock_session)
    assert result == mock_user

def test_get_all_user_not_fount(get_mock_session):
    get_mock_session.query.return_value.all.return_value = []
    with pytest.raises(UserNotFoundException):
        get_all_user(get_mock_session)

@patch("service.user_service.create_access_token")
@patch("service.user_service.verify_password")
def test_get_user_by_email_id(mock_verify_password, mock_create_token, get_mock_session, mock_user, mock_login_form):
    get_mock_session.query.return_value.filter.return_value.first.return_value = mock_user
    mock_verify_password.return_value = True
    mock_create_token.return_value = "fake-jwt-token"

    result = get_user_by_user_email(mock_login_form, get_mock_session)

    assert result == {"access_token": "fake-jwt-token", "token_type": "bearer"}
    mock_verify_password.assert_called_once_with(mock_login_form.password, mock_user.password)
    mock_create_token.assert_called_once_with(data={"sub": mock_user.user_email})

def test_get_user_by_user_email_invalid_username(get_mock_session, mock_login_form):
    get_mock_session.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(InvalidCredentialException) as excinfo:
        get_user_by_user_email(mock_login_form, get_mock_session)

    assert str(excinfo.value) == "Invalid username. Please enter Valid email Id"

@patch("service.user_service.verify_password")
def test_get_user_by_user_email_invalid_password(mock_verify_password, get_mock_session, mock_user, mock_login_form):
    get_mock_session.query.return_value.filter.return_value.first.return_value = mock_user
    mock_verify_password.return_value = False

    with pytest.raises(InvalidCredentialException) as excinfo:
        get_user_by_user_email(mock_login_form, get_mock_session)

    assert str(excinfo.value) == "Invalid password. Please enter valid Password"
    mock_verify_password.assert_called_once_with(mock_login_form.password, mock_user.password)   

def test_create_user_already_exists(get_mock_session, mock_user):
    get_mock_session.query.return_value.filter.return_value.first.return_value = Users()

    with pytest.raises(UserAlreadyExistsException):
        create_user(mock_user, get_mock_session)

@patch("service.user_service.hash_password")
@patch("service.user_service.create_access_token")
def test_create_user(mock_create_token, mock_hash_password,get_mock_session, mock_create_user):
    get_mock_session.query.return_value.filter.return_value.first.return_value = None

    
    mock_hash_password.return_value = "dummyhashedpassword"
    mock_create_token.return_value = "fake-jwt-token"

    result = create_user(mock_create_user, get_mock_session)

    
    get_mock_session.add.assert_called_once()
    get_mock_session.commit.assert_called_once()
    get_mock_session.refresh.assert_called_once()

    
    mock_hash_password.assert_called_once_with(mock_create_user.user_password)
    mock_create_token.assert_called_once()

    
    assert result == {"access_token": "fake-jwt-token", "token_type": "bearer"}




def test_update_user(mock_user,get_mock_session, mock_create_user):
    get_mock_session.get.return_value = mock_user
    result = update_user_details(1, mock_create_user, get_mock_session)
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
    get_mock_session.get.return_value = mock_user
    result = delete_user_detail(mock_user_id, get_mock_session)   
    get_mock_session.delete.assert_called_once_with(mock_user)
    get_mock_session.commit.assert_called_once()
    assert result == {"message": "User deleted successfully"}

def test_delete_user_not_found(get_mock_session):
    get_mock_session.get.return_value = []
    with pytest.raises(UserNotFoundException):
        delete_user_detail(mock_user_id, get_mock_session)    