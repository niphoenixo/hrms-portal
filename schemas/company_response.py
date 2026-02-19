from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional, Dict, Any,List
from datetime import datetime
from .generic_schema import GenericResponse
class CompanyResponse(BaseModel):
    company_uuid: str
    company_name: str
    company_registration_no: str
    company_type: str
    company_type_meta: str
    company_web: Optional[str] = None
    company_logo: Optional[str] = None
    comapany_email: str 
    company_contact_no: str
    company_gst_no: Optional[str] = None
    company_pan_no: str
    company_tin_no: str
    company_cin_no: str
    company_country: str
    company_meta: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime
    created_by: str
    updated_by: str
    
    is_active: Any 

    model_config = ConfigDict(from_attributes=True)

    @field_validator("is_active", mode="before")
    @classmethod
    def transform_active_status(cls, v: Any) -> str:
        # 0 = inactive, 1 = active, 2 = hold, 3 = deleted
        status_map = {0: "inactive", 1: "active", 2: "hold", 3: "deleted"}
        return status_map.get(v, "active")
    

CompanyResponseEnvelope = GenericResponse[CompanyResponse]

