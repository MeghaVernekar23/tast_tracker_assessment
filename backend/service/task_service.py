
from datetime import date
from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from db.models.db_models import Tasks, Users, UserTask
from db.models.pydantic_models import (TaskCreate, TasksPydantic, TaskUpdate,
                                       UserTaskPydantic)
from exceptions import TaskNotFoundException, UserNotFoundException


def get_user_tasks_details(user_email: str, db: Session):
    user = db.query(Users).filter(Users.user_email == user_email).first()
    if not user:
        raise UserNotFoundException()

    user_tasks = (
        db.query(UserTask)
        .join(UserTask.task)
        .filter(UserTask.user_id == user.user_id)
        .all()
    )

    return [
        UserTaskPydantic(
            task_id=ut.task.task_id,
            task_name=ut.task.task_name,
            task_desc=ut.task.task_desc,
            task_category=ut.task.task_category,
            assigned_date = ut.assigned_date,
            due_date=ut.due_date,
            status=ut.status
        )
        for ut in user_tasks
    ]

def create_task(task: TaskCreate, db: Session, user_email:str):

    try:
        user = db.query(Users).filter(Users.user_email == user_email).first()
        if not user:
            raise UserNotFoundException()
        new_task = Tasks(
                task_name=task.task_name,
                task_desc=task.task_desc,
                task_category=task.task_category
            )
        db.add(new_task)
        db.commit()
        db.refresh(new_task)

        new_user_task = UserTask(
                user_id=user.user_id,  
                task_id=new_task.task_id,
                assigned_date=date.today(),
                due_date=task.due_date,
                status="Pending"
            )
        db.add(new_user_task)
        db.commit()
        return {"message": "Task created and assigned successfully."}
    except UserNotFoundException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create task: {str(e)}")


def update_task_detail(editingTaskId: int,task_data: TaskUpdate, db: Session):
    try:
        task = db.get(Tasks,editingTaskId)
        if not task:
            raise TaskNotFoundException()
        
        user_task = db.query(UserTask).filter(UserTask.task_id == task.task_id).first()
        if not user_task:
            raise TaskNotFoundException() 
        task.task_name = task_data.task_name
        task.task_desc = task_data.task_desc
        task.task_category = task_data.task_category

        db.add(task)

    
        user_task.due_date = task_data.due_date
        user_task.status = task_data.status

        db.add(user_task)

    
        db.commit()
        db.refresh(task)
        return {"message": "Task Updated successfully."}
    except TaskNotFoundException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create task: {str(e)}")


def delete_task_detail(task_id: int,db: Session):
    try:
        task = db.get(Tasks,task_id)
        if not task:
            raise TaskNotFoundException()
        
        user_task = db.query(UserTask).filter(UserTask.task_id == task.task_id).first()

        if not user_task:
            raise TaskNotFoundException()
        
        db.delete(task)
        db.delete(user_task)
        db.commit()
        return {"message": "Task deleted successfully"}
    except TaskNotFoundException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def get_all_tasks(db: Session)-> List[TasksPydantic]:

    tasks = db.query(Tasks).all()
    if not tasks:
        raise TaskNotFoundException()
    return tasks





