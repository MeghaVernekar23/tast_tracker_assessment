import traceback
from fastapi import FastAPI, HTTPException, Query
from pydantic import HttpUrl
from db.sessions import get_db, create_tables
from sqlalchemy.orm import Session
from typing import List
from db.models.db_models import Users
from db.models.pydantic_models import UsersPydantic
from db.models.pydantic_models import UserCreate
from fastapi import Depends

from exceptions import UserNotFoundException
from service.user_service import get_all_user
from service.user_service import get_user_by_id
from service.user_service import get_user_by_username
from service.user_service import create_user
from service.user_service import update_user_details
from service.user_service import delete_user_detail
import uvicorn

app = FastAPI()

create_tables()

@app.get("/users",response_model = List[UsersPydantic])    
async def get_user_details(db: Session = Depends(get_db)):
    try:
         return get_all_user(db=db)
    except Exception as e:
         raise HTTPException(status_code=500, detail=str(e))
   
@app.get("/{user_id}",response_model = UsersPydantic)
async def get_user_by_userid(user_id: int, db: Session = Depends(get_db)):
    try:
        return get_user_by_id(user_id=user_id,db=db)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/users/by-name",response_model = List[UsersPydantic])
async def get_user_by_name(user_name: str = Query(...), db: Session = Depends(get_db)):
    try:
        return get_user_by_username(user_name = user_name, db = db)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/",response_model= UsersPydantic)
async def add_user(user: UserCreate ,db: Session = Depends(get_db)):
    try:
        return create_user(user=user,db=db)
    except:
        raise HTTPException(status_code=500, detail="Error Occured while create a new user")     

@app.put("/{user_id}",response_model = UsersPydantic)
async def update_user(user_id : int , user_data: UserCreate ,db: Session = Depends(get_db)):
    try:
        return update_user_details(user_id=user_id,user_data=user_data,db=db)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e)) 
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code= 500,detail= "Error Occured while updating a new user" )   
    

@app.delete("/{user_id}")
async def delete_user(user_id: int,db: Session = Depends(get_db)):
    try:
        return delete_user_detail(user_id=user_id,db=db)
    except UserNotFoundException as e:
        raise HTTPException(status_code=500, detail= "Error Occured while deleting a new user" ) 