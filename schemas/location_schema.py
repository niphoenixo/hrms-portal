from pydantic import BaseModel, ConfigDict, Field,field_validator
from datetime import datetime
from typing import Optional,List,Any

class LocationBase(BaseModel):
    is_primary_address: bool = Field(default=False, description="1 for primary, 0 for non")
    location_address: str = Field(..., description="Full location address")
    location_city: str = Field(..., max_length=50)
    location_state: str = Field(..., max_length=50)
    location_pin_code: str = Field(..., max_length=15)
    location_country: str = Field(..., max_length=50)
    is_active_location: int = Field(default=1, description="0: inactive, 1: active, 2: hold, 3: deleted")

class LocationCreate(LocationBase):
    company_id: int
   

class LocationUpdate(BaseModel):
    is_primary_address: Optional[bool] = None
    location_address: Optional[str] = None
    location_city: Optional[Optional[str]] = None
    location_state: Optional[str] = None
    location_pin_code: Optional[str] = None
    location_country: Optional[str] = None
    is_active_location: Optional[int] = None
    updated_by: str 

# Schema for returning data (Output to User)
class LocationResponse(LocationBase):
    
    location_uuid: str
    created_by: str
    updated_by: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
    @field_validator("is_active_location", mode="before")
    @classmethod
    def transform_active_status(cls, v: Any) -> str:
        status_map = {0: "inactive", 1: "active", 2: "hold", 3: "deleted"}
        if isinstance(v, int):
            return status_map.get(v, "active")
        return v

class LocationResponseEnvelope(LocationResponse):
    message: str
    trace_id: str
    data: List[LocationResponse]
    

    