
from sqlalchemy import Column, Integer, String, LargeBinary
from sqlalchemy.orm import declarative_base


Base = declarative_base()

class Users(Base):
    __tablename__ = "users"
    user_id = Column(Integer,primary_key=True)
    user_name = Column(String)
    user_address = Column(String)
    user_phone_no = Column(String, unique=True)
    user_email = Column(String, unique=True)
    password = Column(String)

class Tasks(Base):
    __tablename__ = "tasks"
    task_id = Column(Integer,primary_key = True) 
    task_name = Column(String)
    task_desc = Column(String)
    task_category = Column(String)

class Documents(Base):
    __tablename__ = "documents"    
    document_id = Column(Integer,primary_key = True)
    document_name = Column(String)
    document_type = Column(String)
    document_data = Column(LargeBinary)

