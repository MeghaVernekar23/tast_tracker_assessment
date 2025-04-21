
from unittest.mock import MagicMock
from urllib import response
from fastapi.testclient import TestClient
from db.models.pydantic_models import UsersPydantic, UserCreatePydantic
from db.sessions import get_db
from backend.main import app
from backend.main import user_router
from pytest import MonkeyPatch

app.include_router(user_router)

client = TestClient(app)

mock_users = [
    UsersPydantic(user_id = 1,user_name = "Megha", user_address = "Mysore", user_phone_no = "9977664463")
]

mock_user = MagicMock()
mock_user.user_id = 1
mock_user.user_name = "Megha"
mock_user.user_address = "Mysore"
mock_user.user_phone_no = "9977664463"


mock_db = MagicMock()
mock_query = MagicMock()
mock_query.all.return_value = mock_users
mock_db.query.return_value = mock_query
mock_query.add.return_value = None
mock_query.commit.return_value = None
mock_db.refresh.side_effect = lambda u: u.__dict__.update(mock_user.__dict__)

MonkeyPatch()


def overide_db():
    return mock_db


app.dependency_overrides[get_db] = overide_db


def test_get_users():
    response = client.get("/users")
    assert response.status_code == 200
    for user in response.json():
        assert user["user_id"] == 1
        assert user["user_name"] == "Megha"
        assert user["user_address"] == "Mysore"
        assert user["user_phone_no"] == "9977664463"

    
def test_create_user():
    response = client.post("/" , json={
            "user_name": "Megha",
            "user_address": "Mysore",
            "user_phone_no": "9977664463"
        }) 
    assert response.status_code == 200   

def test_crea22te_user():
    response = client.post("/" , json={
            "user_name": "Megha",
            "user_address": "Mysore",
            "user_phone_no": "9977664463"
        }) 
    assert response.status_code == 200   

