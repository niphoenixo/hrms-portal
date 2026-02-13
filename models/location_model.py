from sqlalchemy import Column, String, DateTime, ForeignKey, Index, Boolean
from sqlalchemy.dialects.mysql import BIGINT, TINYINT, MEDIUMTEXT
from sqlalchemy.sql import func
from database.db import Base


class Location(Base):
    __tablename__ = 'locations'

    id = Column(
        BIGINT(unsigned=True), 
        primary_key=True, 
        autoincrement=True, 
        nullable=False
    )
    
    company_id = Column(
        BIGINT(unsigned=True), 
        ForeignKey('companies.id'), 
        nullable=False, 
        comment='companies table id'
    )
    
    location_uuid = Column(String(36), nullable=False)
    
    is_primary_address = Column(
        Boolean, 
        nullable=False, 
        server_default='0', 
        comment='1 for primery ,0 for non'
    )
    
    location_address = Column(
        MEDIUMTEXT, 
        nullable=False, 
        comment='location address'
    )
    
    location_city = Column(String(50), nullable=False)
    location_state = Column(String(50), nullable=False)
    location_pin_code = Column(String(15), nullable=False)
    location_country = Column(String(50), nullable=False)
    
    created_by = Column(String(36), nullable=False)
    updated_by = Column(String(36), nullable=False)
    
    is_active_location = Column(
        TINYINT, 
        nullable=False, 
        server_default='0', 
        comment='0 for inactive,1 for active ,2 for hold, 3 for deleted'
    )
    
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    __table_args__ = (
        Index('locations_company_id_index', 'company_id'),
        Index('locations_location_uuid_index', 'location_uuid'),
    )