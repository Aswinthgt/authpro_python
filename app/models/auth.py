from pydantic import BaseModel, EmailStr
from typing import Optional, Union

class authData(BaseModel):
    user_name: str
    password: str
    email: Optional[EmailStr] = None

class authVerify(BaseModel):
    email: str
    otp: Optional[Union[int , str]]