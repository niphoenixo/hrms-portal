import io
import uuid
from fastapi import APIRouter,Request,UploadFile,File,Depends
from bulk.comapny_data import generate_company_data
from database.context import trace_id
from database.db import get_db
from sqlalchemy.orm import Session
import pandas as pd
from schemas.company_schema import CompanyCreate
from pydantic import ValidationError
from custom_response.json_response import CustomJSONResponse
import json

router = APIRouter(
    prefix="/bulk",
    tags=["bulk company"]
)

@router.get("/upload-company")
def get_company():
    return {
        "message": "bulk", 
        "data":None, 
        "trace_id": trace_id.get()
    }
@router.post("/upload-company")
async def upload_company(request: Request,file_name: UploadFile = File(...), db: Session = Depends(get_db)):
    get_file_name=file_name.filename
    if not get_file_name.endswith('.csv'):
        return CustomJSONResponse.from_not_found("File must be a CSV")
    
    contents = await file_name.read()
    df = pd.read_csv(io.BytesIO(contents))
    company_count = len(df)
    msg="Empty File"
   
    if company_count > 0:
         #add db colums in csv file
        df['company_uuid'] = [str(uuid.uuid4()) for _ in range(len(df))]
        df['created_by'] = request.state.created_by
        df['updated_by'] = request.state.updated_by

    records = df.replace({pd.NA: None, float('nan'): None}).to_dict(orient="records")
    try:
        validated_records = [CompanyCreate(**row).model_dump() for row in records]
   
    except ValidationError as e:
            return CustomJSONResponse(
                    message=f"Duplicate registration No  found"
                    ).from_pydantic_error(e)
    except Exception as e:
                return CustomJSONResponse.from_server_error(e,"Exception found create company bulk")

    data = generate_company_data(get_file_name,df,db)
    if isinstance(data, dict):

        if "status" in data:
            msg = "Successfull"
            return {
                "message": msg,
                "detail":{
                            "old_file_name":get_file_name,
                            "count_records":company_count,
                            "data":data
                        },
                "trace_id": trace_id.get()
            }
        else:
            return json.loads(data.body)
    else:
         return json.loads(data.body)