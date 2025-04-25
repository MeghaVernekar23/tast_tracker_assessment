
from fastapi import APIRouter, HTTPException, Query,Depends

from db.sessions import get_db, create_tables
from sqlalchemy.orm import Session
from typing import List
from db.models.pydantic_models import Token, UserLogin, UsersPydantic,UserCreatePydantic
from exceptions import UserAlreadyExistsException, UserNotFoundException, InvalidCredentialException
from fastapi.security import OAuth2PasswordRequestForm

from service.user_service import get_all_user
from service.user_service import get_user_by_id
from service.user_service import get_user_by_username
from service.user_service import create_user
from service.user_service import update_user_details
from service.user_service import delete_user_detail, get_user_by_user_email
from service.auth import get_current_user

user_router = APIRouter()

create_tables()

@user_router.get("/users/me")
async def read_protected_data(current_user: str = Depends(get_current_user)):
    return {"user_email": current_user}

@user_router.get("/users",response_model = List[UsersPydantic], dependencies=[Depends(get_current_user)])    
async def get_user_details(db: Session = Depends(get_db)):
    try:
         return get_all_user(db=db)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
         raise HTTPException(status_code=500, detail=str(e))
   
@user_router.get("/users/{user_id}",response_model = UsersPydantic, dependencies=[Depends(get_current_user)])
async def get_user_by_userid(user_id: int, db: Session = Depends(get_db)):
    try:
        return get_user_by_id(user_id=user_id,db=db)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@user_router.get("/users/by-name",response_model = List[UsersPydantic], dependencies=[Depends(get_current_user)])
async def get_user_by_name(user_name: str = Query(...), db: Session = Depends(get_db)):
    try:
        return get_user_by_username(user_name = user_name, db = db)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@user_router.post("/users/signup",response_model= Token)
async def add_user(user: UserCreatePydantic ,db: Session = Depends(get_db)):
    
    try:
        return create_user(user=user,db=db)
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error Occured while create a new user")     
    
@user_router.post("/users/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    try:
        return get_user_by_user_email(user= form_data, db= db)
    except InvalidCredentialException as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error Occured while Login in") 
        


@user_router.put("/users/{user_id}",response_model = UsersPydantic, dependencies=[Depends(get_current_user)])
async def update_user(user_id : int , user_data: UserCreatePydantic ,db: Session = Depends(get_db)):
    try:
        return update_user_details(user_id=user_id,user_data=user_data,db=db)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e)) 
    except Exception as e:
        raise HTTPException(status_code= 500,detail= "Error Occured while updating a user" )   
    

@user_router.delete("/users/{user_id}", dependencies=[Depends(get_current_user)])
async def delete_user(user_id: int,db: Session = Depends(get_db)):
    try:
        return delete_user_detail(user_id=user_id,db=db)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e)) 
    except Exception as e:
        raise HTTPException(status_code= 500,detail= "Error Occured while deleting the user" )   
    

