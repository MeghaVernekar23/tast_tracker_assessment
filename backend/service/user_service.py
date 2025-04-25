from db.models.pydantic_models import UserLogin, UsersPydantic
from sqlalchemy.orm import Session
from typing import List
from db.models.db_models import Users
from db.models.pydantic_models import UsersPydantic
from db.models.pydantic_models import UserCreatePydantic
from exceptions import UserNotFoundException, UserAlreadyExistsException, InvalidCredentialException
from fastapi.security import OAuth2PasswordRequestForm

from service.auth import hash_password, create_access_token, verify_password

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

def get_user_by_user_email(user: OAuth2PasswordRequestForm , db: Session) -> dict:
  
    print("Login attempt with:", user.username)
    user_detail =  db.query(Users).filter(Users.user_email == user.username).first()

    if not user_detail:
        raise InvalidCredentialException("Invalid username")   
    
    if not verify_password(user.password, user_detail.password): 
        raise InvalidCredentialException("Invalid password")
    
    access_token = create_access_token(data={"sub": user_detail.user_email})
    return {"access_token": access_token, "token_type": "bearer"}


def create_user(user: UserCreatePydantic , db: Session) -> dict:
    """Create users"""
    existing_user = db.query(Users).filter(Users.user_email == user.user_email).first()

    if existing_user:
        raise UserAlreadyExistsException()
    
    hashed_pwd = hash_password(user.user_password)

    new_user_data = Users(user_name=user.user_name,user_address=user.user_address,
                     user_phone_no=user.user_phone_no,user_email=user.user_email,password=hashed_pwd)
    
    db.add(new_user_data)
    db.commit()
    db.refresh(new_user_data)
    access_token = create_access_token(data={"sub": new_user_data.user_name})

    return {"access_token": access_token, "token_type": "bearer"}

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
