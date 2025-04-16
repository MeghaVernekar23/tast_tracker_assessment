from pydantic import BaseModel
from typing import Optional

class UsersPydantic(BaseModel):
    user_id: int
    user_name: str
    user_address: str
    user_phone_no: str



class UserCreate(BaseModel):
    user_name: str
    user_address: Optional[str]
    user_phone_no: str    