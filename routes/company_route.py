from fastapi import APIRouter, Depends, HTTPException, status,Request
from sqlalchemy.orm import Session
from database.db import get_db
from models import Company
from database.context import trace_id
import uuid
from schemas.company_response import CompanyResponseEnvelope
from schemas.company_schema import CompanyCreate
from services.company.company_service import CompanyService
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from custom_response.json_response import CustomJSONResponse

router = APIRouter(
    prefix="/company",
    tags=["company"]
)

@router.get("/list")
def get_company_list(db: Session = Depends(get_db)):
    service = CompanyService(db)
    companies = service.get_company_list()    
    if not companies:
        return CustomJSONResponse.from_not_found("companies list")
    
    return {
        "message": "Companies List", 
        "data": companies, 
        "trace_id": trace_id.get()
    }

@router.get("/{company_uuid}", response_model=CompanyResponseEnvelope)
def get_company(company_uuid: str, db: Session = Depends(get_db)):
    customRes = CustomJSONResponse()
    service = CompanyService(db)
    company = service.get_company(company_uuid)    
    if not company:
        return CustomJSONResponse.from_not_found("Company")
    
    return {
        "message": "Company Detail", 
        "data": [company], 
        "trace_id": trace_id.get()
    }

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_company(company_in: CompanyCreate, request: Request, db: Session = Depends(get_db)):
        customRes = CustomJSONResponse()
        try:
            body = await request.json()
            company_in = CompanyCreate.model_validate(body, context={"db": db})
        except ValidationError as e:
            return CustomJSONResponse(
                    message=f"Duplicate registration No {body.get('company_registration_no')} found"
                    ).from_pydantic_error(e)
        except Exception as e:
                return CustomJSONResponse.from_server_error(e,"Exception found create company")
         
        company_dict = company_in.model_dump()
        company_dict["company_uuid"] = str(uuid.uuid4())
        company_dict["created_by"] = request.state.created_by
        company_dict["updated_by"] = request.state.updated_by

        service = CompanyService(db)
        created_record = service.create_company(company_dict) 

        return {
            "message": "Company created successfully", 
            "data": {
                "company_uuid": created_record.company_uuid
            },
            "trace_id": trace_id.get()
        }


@router.put("/{id}")
def update_company(id: str, company_update: dict, db: Session = Depends(get_db)):
    company_query = db.query(Company).filter(Company.id == id)
    company = company_query.first()
    
    if not company:
        return CustomJSONResponse.from_not_found("Company")
    
    company_query.update(company_update, synchronize_session=False)
    db.commit()
    return {"message": "Company updated successfully"}