from pydantic import BaseModel, ConfigDict, Field, EmailStr,field_validator,ValidationInfo
from datetime import datetime
from typing import Optional, Any, Dict
from sqlalchemy.orm import Session
class AuditMixin(BaseModel):
    created_by: str
    updated_by: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class CompanyBase(BaseModel):

    company_name: str
    company_registration_no: str
    company_type: str = "private"
    company_type_meta: str
    company_web: Optional[str] = None
    company_logo: Optional[str] = None
    comapany_email: EmailStr
    company_contact_no: str
    company_gst_no: Optional[str] = None
    company_pan_no: str
    company_tin_no: str
    company_cin_no: str
    company_meta: Optional[Dict[str, Any]] = None
    company_country: str
    @field_validator("company_type_meta")
    @classmethod
    def validate_type_meta(cls, v: str) -> str:
        allowed = ["software", "it", "manufacturing", "education"]
        val = v.lower().strip()
        if val not in allowed:
            raise ValueError(f"Invalid company_type_meta. Must be one of: {', '.join(allowed)}")
            
        return val
    
    @field_validator('company_registration_no')
    @classmethod
    def validate_unique_registration(cls, v: str, info: ValidationInfo) -> str:
        db: Optional[Session] = info.context.get("db") if info.context else None
        
        if db:
            from models.company_model import Company 
            
            exists = db.query(Company).filter(Company.company_registration_no == v).first()
            if exists:
                raise ValueError(f"Registration number '{v}' is already registered.")
        
        return v
    
class CompanyCreate(CompanyBase):
    # created_by: str
    # updated_by: str
    pass

class CompanyRead(CompanyBase, AuditMixin):
    id: int

class DepartmentBase(BaseModel):
    department_uuid: str
    department_name: str
    is_active_department: int = 0

class DepartmentRead(DepartmentBase, AuditMixin):
    id: str
    company_id: int

class DesignationBase(BaseModel):
    designation_uuid: str
    designation_name: str
    designation_level: str

class DesignationRead(DesignationBase, AuditMixin):
    id: int
    company_id: int

class WorkTypeBase(BaseModel):
    work_type_uuid: str
    work_type: str # remote, hybrid, onsite
    is_active: int = 0

class WorkTypeRead(WorkTypeBase, AuditMixin):
    id: int
    company_id: int

class JobTypeBase(BaseModel):
    job_type_uuid: str
    job_type: str # full time, part time
    is_active: int = 0

class JobTypeRead(JobTypeBase, AuditMixin):
    id: int
    company_id: int

class ActionBase(BaseModel):
    action_uuid: str
    action_name: str
    is_active: int = 0

class ActionRead(ActionBase, AuditMixin):
    id: int
    company_id: int

class CompanyEmpActionRead(AuditMixin):
    id: int
    company_id: int
    location_id: int
    company_action_id: int
    emp_id: int
    is_active_shift_location: int

class CompanyLocationDepartmentRead(AuditMixin):
    id: int
    company_id: int
    location_id: int
    department_id: int
    is_active_location_department: int