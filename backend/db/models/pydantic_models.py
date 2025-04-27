from pydantic import BaseModel, ConfigDict
from typing import Optional
from enum import Enum
from datetime import datetime

class UsersPydantic(BaseModel):
    user_id: int
    user_name: str
    user_address: str
    user_phone_no: str
    user_email: str

    model_config = ConfigDict(from_attributes=True)


class UserCreatePydantic(BaseModel):
    user_name: str
    user_address: Optional[str]
    user_phone_no: str
    user_email: str
    user_password: str    

class TaskCategoryEnum(str,Enum):
     FITNESS = "fitness"
     STUDY = "study"
     OTHERS = "others"

class TasksPydantic(BaseModel):
    task_id : int 
    task_name : str
    task_desc : str
    task_category : TaskCategoryEnum 

class TaskCreatePydantic(BaseModel):
    task_name: str
    task_desc: Optional[str]
    task_category: TaskCategoryEnum   

class TaskStatusEnum(str, Enum):
    Pending = "Pending"
    In_progress = "In Progress"
    Completed = "Completed"    

class UserTaskPydantic(BaseModel):
    task_id: int
    task_name: str
    task_desc: Optional[str]
    task_category: TaskCategoryEnum
    assigned_date: Optional[datetime]
    due_date: Optional[datetime]
    status: TaskStatusEnum


class DocumentType(Enum):
    PDF =  "pdf"
    TEXT = "txt" 

class DocumentPydantic(BaseModel):
    document_id : int
    document_name : str
    document_type : DocumentType
    document_data : str

class UserLogin(BaseModel):
    user_email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
