from pydantic import BaseModel
from typing import Union

class UserRequest(BaseModel):
    address: str
    email: str

class UserUpdate(BaseModel):
    address: Union[str,None] = None
    email: Union[str,None] = None
    is_active: Union[bool,None] = None