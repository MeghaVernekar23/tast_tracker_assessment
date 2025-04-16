from fastapi import FastAPI, HTTPException,Depends
from db.sessions import get_db, create_tables
from sqlalchemy.orm import Session
from typing import List
from db.models.pydantic_models import TasksPydantic, TaskCreate
from service.task_service import get_all_tasks, create_task, update_task_detail, delete_task_detail
from exceptions import TaskNotFoundException

app = FastAPI()

create_tables()


@app.get("/tasks",response_model = List[TasksPydantic])    
async def get_user_details(db: Session = Depends(get_db)):
    try:
         return get_all_tasks(db=db)
    except TaskNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
         raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/",response_model= TasksPydantic)
async def add_task(task: TaskCreate ,db: Session = Depends(get_db)):
    try:
        return create_task(task=task,db=db)
    except:
        raise HTTPException(status_code=500, detail="Error Occured while create a new Task")       
    
@app.put("/{task_id}",response_model = TasksPydantic)
async def update_task(task_id: int,task_data: TaskCreate, db: Session = Depends(get_db)):
    try:
        return update_task_detail(task_id= task_id, task_data = task_data, db= db)
    except TaskNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
         raise HTTPException(status_code=500, detail=str(e))

@app.delete("/{task_id}")
async def delete_user(task_id: int,db: Session = Depends(get_db)):
    try:
        return delete_task_detail(task_id=task_id,db=db)
    except TaskNotFoundException as e:
        raise HTTPException(status_code=500, detail= "Error Occured while deleting a Task" ) 