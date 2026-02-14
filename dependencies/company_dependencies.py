from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
from models.company_model import Company
from custom_response.json_response import CustomJSONResponse

def get_valid_company(company_uuid: str, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.company_uuid == company_uuid).first()
    if not company:
         return None
    return company