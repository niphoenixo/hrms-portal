from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import Optional
from datetime import datetime

class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    company_id: int
    designation_id: Optional[int] = None
    department_id: Optional[int] = None

class EmployeeCreate(EmployeeBase):
    password: str 

class EmployeeResponse(EmployeeBase):
    id: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)