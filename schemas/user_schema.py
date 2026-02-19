from pydantic import BaseModel,  EmailStr
from typing import List
from .generic_schema import GenericResponse
class UserRegister(BaseModel):
    employee_id:int
    user_name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    email: EmailStr
    user_name: str

UserRegistrationResponse = GenericResponse[UserResponse]
UserLoginResponse = GenericResponse[UserResponse]
   