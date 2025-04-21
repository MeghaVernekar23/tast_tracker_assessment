
from typing import List
from sqlalchemy.orm import Session
from backend.db.models.db_models import Tasks
from backend.db.models.pydantic_models import TasksPydantic, TaskCreatePydantic
from backend.exceptions import TaskNotFoundException


def get_all_tasks(db: Session)-> List[TasksPydantic]:

    tasks = db.query(Tasks).all()
    if not tasks:
        raise TaskNotFoundException()
    return tasks

def create_task(task: TaskCreatePydantic, db: Session)-> TasksPydantic:
    new_task = Tasks(**task.dict()) 
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

def update_task_detail(task_id: int,task_data: TaskCreatePydantic, db: Session)-> TasksPydantic:
    task = db.get(Tasks,task_id)
    if not task:
        raise TaskNotFoundException()
    for key, value in task_data.dict(exclude_unset=True).items():
        setattr(task, key, value)
    db.add(task)    
    db.commit()
    db.refresh(task)
    return task


def delete_task_detail(task_id: int,db: Session):
    task = db.get(Tasks,task_id)
    if not task:
        raise TaskNotFoundException()
    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}