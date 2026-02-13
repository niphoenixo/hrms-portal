from sqlalchemy.orm import Session
from models import Company
class CompanyService:
    def __init__(self, db: Session):
        self.db = db

    def get_company_list(self):
        return self.db.query(Company).all()
    
    def create_company(self, data: dict):
        db_company = Company(**data)
        self.db.add(db_company)
        self.db.commit()
        self.db.refresh(db_company)
        return db_company 
    
    def get_company(self, company_uuid:str):
        return self.db.query(Company).filter(Company.company_uuid == company_uuid).first()