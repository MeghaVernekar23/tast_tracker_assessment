
from sqlalchemy import Column, Integer, String, LargeBinary, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Enum as SQLAlchemyEnum
from db.models.pydantic_models import TaskStatusEnum


Base = declarative_base()


class UserTask(Base):
    __tablename__ = "user_tasks"
    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    task_id = Column(Integer, ForeignKey("tasks.task_id"), primary_key=True)
    assigned_date = Column(DateTime)
    due_date = Column(DateTime)
    status = Column(SQLAlchemyEnum(TaskStatusEnum), default=TaskStatusEnum.Pending)

    user = relationship("Users", back_populates="user_tasks")
    task = relationship("Tasks", back_populates="user_tasks")

     
class Users(Base):
    __tablename__ = "users"
    user_id = Column(Integer,primary_key=True)
    user_name = Column(String)
    user_address = Column(String)
    user_phone_no = Column(String, unique=True)
    user_email = Column(String, unique=True)
    password = Column(String)

    user_tasks = relationship("UserTask", back_populates="user", cascade="all, delete-orphan")

class Tasks(Base):
    __tablename__ = "tasks"
    task_id = Column(Integer,primary_key = True) 
    task_name = Column(String)
    task_desc = Column(String)
    task_category = Column(String)

    user_tasks = relationship("UserTask", back_populates="task", cascade="all, delete-orphan")

class Documents(Base):
    __tablename__ = "documents"    
    document_id = Column(Integer,primary_key = True)
    document_name = Column(String)
    document_type = Column(String)
    document_data = Column(LargeBinary)

