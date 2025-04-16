from pydantic import BaseModel
from typing import Optional
from enum import Enum
from typing import List
class UsersPydantic(BaseModel):
    user_id: int
    user_name: str
    user_address: str
    user_phone_no: str
class UserCreate(BaseModel):
    user_name: str
    user_address: Optional[str]
    user_phone_no: str    

class TaskCategoryEnum(str,Enum):
     FITNESS = "fitness"
     STUDY = "study"
     OTHERS = "others"

class TasksPydantic(BaseModel):
    task_id : int 
    task_name : str
    task_desc : str
    task_category : TaskCategoryEnum 

class TaskCreate(BaseModel):
    task_name: str
    task_desc: Optional[str]
    task_category: TaskCategoryEnum        

