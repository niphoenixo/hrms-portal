from pydantic import BaseModel,  EmailStr

class UserRegister(BaseModel):
    employee_id:int
    user_name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str