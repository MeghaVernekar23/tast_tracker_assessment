from db.models.pydantic_models import UsersPydantic
from sqlalchemy.orm import Session
from typing import List
from db.models.db_models import Users
from db.models.pydantic_models import UsersPydantic
from db.models.pydantic_models import UserCreate
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


def get_user_by_username(user_name: int , db: Session) -> UsersPydantic:
    """Get list of User by user name"""
    user =  db.query(Users).filter(Users.user_name == user_name).all()
    if not user:
        raise UserNotFoundException()
    return user


def create_user(user: UserCreate , db: Session) -> UsersPydantic:
    """Get list of User by user name"""
    new_user = Users(**user.dict()) 
    db.add(new_user)
    db.commit()
    return new_user

def update_user_details(user_id: int, user_data:UserCreate, db: Session)-> UsersPydantic:
    
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
    user =  db.get(Users, user_id)
    if not user:
         raise UserNotFoundException()
    db.delete(user)
    db.commit()
    return "user deleted Successfully"
