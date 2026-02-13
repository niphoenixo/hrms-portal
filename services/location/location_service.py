from sqlalchemy.orm import Session
from models import Location

class LocationService:
    def __init__(self, db: Session):
        self.db = db

    def create_location(self, data: dict):
        db_location = Location(**data)
        self.db.add(db_location)
        self.db.commit()
        self.db.refresh(db_location)
        return db_location 
    
    def get_location(self, location_uuid:str):
        return self.db.query(Location).filter(Location.location_uuid == location_uuid).first()