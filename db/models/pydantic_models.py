from pydantic import BaseModel, ConfigDict
from typing import Optional
from enum import Enum
from typing import List
class UsersPydantic(BaseModel):
    user_id: int
    user_name: str
    user_address: str
    user_phone_no: str

    model_config = ConfigDict(from_attributes=True)
class UserCreatePydantic(BaseModel):
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

class TaskCreatePydantic(BaseModel):
    task_name: str
    task_desc: Optional[str]
    task_category: TaskCategoryEnum   

class DocumentType(Enum):
    PDF =  "pdf"
    TEXT = "txt" 

class DocumentPydantic(BaseModel):
    document_id : int
    document_name : str
    document_type : DocumentType
    document_data : str


