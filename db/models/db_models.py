
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Users(Base):
    __tablename__ = "users"
    user_id = Column(Integer,primary_key=True)
    user_name = Column(String)
    user_address = Column(String)
    user_phone_no = Column(String, unique=True)

class Tasks(Base):
    __tablename__ = "tasks"
    task_id = Column(Integer,primary_key = True) 
    task_name = Column(String)
    task_desc = Column(String)
    task_category = Column(String)

