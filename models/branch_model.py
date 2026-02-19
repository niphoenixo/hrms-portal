

from sqlalchemy import Column, String, DateTime,ForeignKey
from sqlalchemy.dialects.mysql import BIGINT,TINYINT
from sqlalchemy.sql import func
from database.db import Base


class Branch(Base):
    __tablename__ = 'branches'

    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    company_id = Column(
        BIGINT(unsigned=True), 
        ForeignKey('companies.id'), 
        nullable=False, 
        comment='companies table id'
    )
    location_id = Column(
        BIGINT(unsigned=True), 
        ForeignKey('locations.id'), 
        nullable=False, 
        comment='locations table id'
    )
    branch_uuid = Column(String(36), nullable=False)
    branch_name = Column(String(100), nullable=False)
    branch_email = Column(String(100), nullable=True)
    branch_contact_no = Column(String(100), nullable=True)
    branch_city = Column(String(50), nullable=False)
    branch_state = Column(String(50), nullable=False)
    branch_pin_code = Column(String(15), nullable=False)
    created_by = Column(String(36), nullable=False)
    updated_by = Column(String(36), nullable=False)
    
    is_active_branch = Column(
        TINYINT, 
        nullable=False, 
        server_default='0', 
        comment='0 for inactive,1 for active ,2 for hold, 3 for deleted'
    )
    
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    