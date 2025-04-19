from db.models.pydantic_models import UsersPydantic
from sqlalchemy.orm import Session
from typing import List
from db.models.db_models import Users
from db.models.pydantic_models import UsersPydantic
from db.models.pydantic_models import UserCreatePydantic
from exceptions import UserNotFoundException

def get_all_user(db: Session) -> List[UsersPydantic]:
    """Get list of all Users"""
    users = db.query(Users).all()
    if not users:
        raise UserNotFoundException()
    return users

def get_user_by_id(user_id: int , db: Session) -> UsersPydantic:
    """Get list of User by user id"""
    user =  db.get(Users, user_id)
    if not user:
        raise UserNotFoundException()
    return user


def get_user_by_username(user_name: str , db: Session) -> UsersPydantic:
    """Get list of User by user name"""
    user =  db.query(Users).filter(Users.user_name == user_name).all()
    if not user:
        raise UserNotFoundException()
    return user


def create_user(user: UserCreatePydantic , db: Session) -> UsersPydantic:
    """Create users"""
    new_user = Users(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def update_user_details(user_id: int, user_data:UserCreatePydantic, db: Session)-> UsersPydantic:
    """update users"""
    user =  db.get(Users, user_id)
    if not user:
         raise UserNotFoundException()
    for key, value in user_data.dict(exclude_unset=True).items():
        setattr(user, key, value)
    db.add(user)    
    db.commit()
    db.refresh(user)
    return user
   
def delete_user_detail(user_id: int,db: Session)->str:
    """Delete users"""
    user =  db.get(Users, user_id)
    if not user:
         raise UserNotFoundException()
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
