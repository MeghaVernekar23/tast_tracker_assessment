
from typing import List
from sqlalchemy.orm import Session
from db.models.db_models import Tasks, Users, UserTask
from db.models.pydantic_models import TasksPydantic, TaskCreatePydantic, UserTaskPydantic
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
            due_date=ut.due_date,
            status=ut.status
        )
        for ut in user_tasks
    ]


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