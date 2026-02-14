from fastapi import APIRouter, Depends, status,Request
from sqlalchemy.orm import Session
from database.db import get_db
from models import Location,Company
from database.context import trace_id
import uuid
from services.location.location_service import LocationService
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from custom_response.json_response import CustomJSONResponse
from schemas.location_schema import LocationCreate,LocationResponseEnvelope
from dependencies.company_dependencies import get_valid_company

router = APIRouter(
    prefix="/location",
    tags=["Location"]
)

@router.get("/{company_uuid}/list")
def get_location_list(company_uuid:str,db: Session = Depends(get_db),company: Company = Depends(get_valid_company)):
    locations = db.query(Location).all()
    if not locations:
        return CustomJSONResponse.from_not_found("locations List")
    
    company_detail ={"company_name":company.company_name,"company_uuid":company.company_uuid}
    return {
        "message": "location list", 
        "data": {"company_detail":company_detail,"location_detail":locations},
        "trace_id": trace_id.get()
    }

@router.get("/{location_uuid}",response_model=LocationResponseEnvelope)
def get_location(location_uuid: str, db: Session = Depends(get_db)):
    customRes = CustomJSONResponse()
    service = LocationService(db)
    location = service.get_location(location_uuid)    
    if not location:
        return CustomJSONResponse.from_not_found("location detail")
    
    return {
        "message": "location Detail", 
        "data": [location], 
        "trace_id": trace_id.get()
    }

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_location(location_in: LocationCreate,request: Request, db: Session = Depends(get_db)):
        customRes = CustomJSONResponse()
        try:
            body = await request.json()

        except ValidationError as e:
            return CustomJSONResponse(
                    message=f"Duplicate registration No {location_in.get('company_registration_no')} found"
                    ).from_pydantic_error(e)
        except Exception as e:
                return CustomJSONResponse.from_server_error(e,"Exception found location create")
         
        location_dict = location_in.model_dump()
        location_dict["location_uuid"] = str(uuid.uuid4())
        location_dict["created_by"] = request.state.created_by
        location_dict["updated_by"] = request.state.updated_by

        service = LocationService(db)
        created_record = service.create_location(location_dict) 

        return {
            "message": "location created successfully", 
            "data": {
                "location_uuid": created_record.location_uuid
            },
            "trace_id": trace_id.get()
        }


@router.put("/{location_uuid}")
def update_location(location_uuid: str, location_update: dict, db: Session = Depends(get_db)):
    location_query = db.query(Location).filter(Location.id == id)
    location = location_query.first()
    
    if not location:
        return CustomJSONResponse.from_not_found("Location Update")
    
    location_query.update(location_update, synchronize_session=False)
    db.commit()
    return {"message": "Location updated successfully"}