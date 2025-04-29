from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.models.pydantic_models import (TaskCreate, TaskCreatePydantic,
                                       TasksPydantic, TaskUpdate,
                                       UserTaskPydantic)
from db.sessions import create_tables, get_db
from exceptions import TaskNotFoundException, UserNotFoundException
from service.auth import get_current_user
from service.task_service import (create_task, delete_task_detail,
                                  get_all_tasks, get_user_tasks_details,
                                  update_task_detail)

task_router = APIRouter()

create_tables()


@task_router.get("/logged-user-tasks", response_model = List[UserTaskPydantic], dependencies=[Depends(get_current_user)])    
async def get_logged_user_task_details(current_user: str = Depends(get_current_user),db: Session = Depends(get_db)):
    
    try:
        return get_user_tasks_details(user_email = current_user , db=db )
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail = str(e))
    except HTTPException as e:
        raise HTTPException(status_code=500, detail=str(e))

@task_router.post("/addTask", dependencies=[Depends(get_current_user)])
async def add_task(task: TaskCreate ,current_user: str = Depends(get_current_user),db: Session = Depends(get_db)):
    try:
        return create_task(task=task,db=db, user_email=current_user)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail = str(e))
    except HTTPException as e:
        raise HTTPException(status_code=500, detail=str(e))


@task_router.put("/UpdateTask/{editingTaskId}", dependencies=[Depends(get_current_user)])
async def update_task(editingTaskId: int,task_data: TaskUpdate, db: Session = Depends(get_db)):
    try:
        return update_task_detail(editingTaskId= editingTaskId, task_data = task_data, db= db)
    except TaskNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
         raise HTTPException(status_code=500, detail=f"Failed to create task: {str(e)}")

@task_router.delete("/deleteTask/{task_id}", dependencies=[Depends(get_current_user)])
async def delete_task(task_id: int,db: Session = Depends(get_db)):
    try:
        return delete_task_detail(task_id=task_id,db=db)
    except TaskNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
         raise HTTPException(status_code=500, detail=str(e))

@task_router.get("/tasks", response_model = List[TasksPydantic], dependencies=[Depends(get_current_user)])    
async def get_user_details(db: Session = Depends(get_db)):
    try:
         return get_all_tasks(db=db)
    except TaskNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
         raise HTTPException(status_code=500, detail=str(e))      
    

