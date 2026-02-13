from sqlalchemy import Column, String, DateTime, ForeignKey, Index, Enum, Date
from sqlalchemy.dialects.mysql import BIGINT, TINYINT
from sqlalchemy.sql import func
from database.db import Base



# 3. Employees
class Employee(Base):
    __tablename__ = 'employee'

    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    company_id = Column(BIGINT(unsigned=True), ForeignKey('companies.id'), nullable=False)
    location_id = Column(BIGINT(unsigned=True), ForeignKey('locations.id'), nullable=False)
    location_department_id = Column(BIGINT(unsigned=True), ForeignKey('company_location_department.id'), nullable=False)
    
    emp_uuid = Column(String(36), nullable=False)
    emp_code = Column(String(50), nullable=False)
    emp_contact_no = Column(String(25), nullable=False)
    emp_official_email = Column(String(20), nullable=False)
    date_of_joining = Column(DateTime(timezone=True), nullable=False)
    date_of_leaving = Column(DateTime(timezone=True), nullable=True)
    
    emp_status = Column(TINYINT, server_default='0', nullable=False)
    created_by = Column(String(36), nullable=False)
    updated_by = Column(String(36), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    __table_args__ = (
        Index('idx_emp_company', 'company_id'),
        Index('idx_emp_location', 'location_id'),
        Index('idx_emp_uuid', 'emp_uuid'),
        Index('idx_emp_loc_dept', 'location_department_id'),
    )

# 4. Employee Profiles
class EmployeeProfile(Base):
    __tablename__ = 'employee_profile'

    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    emp_id = Column(BIGINT(unsigned=True), ForeignKey('employee.id'), nullable=False)
    
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    middle_name = Column(String(50), nullable=False)
    gender = Column(Enum('Male', 'Female', 'Other'), nullable=False) # Added common values
    mobile_no = Column(BIGINT, nullable=False) # Changed from INT for phone number length
    emp_dob = Column(Date, nullable=False)
    emp_email = Column(String(50), nullable=False)
    blood_group = Column(String(5), nullable=False)
    emp_marital_status = Column(TINYINT, server_default='0', nullable=False)
    
    emp_profile_status = Column(TINYINT, server_default='0', nullable=False)
    created_by = Column(String(36), nullable=False)
    updated_by = Column(String(36), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    __table_args__ = (
        Index('idx_ep_emp', 'emp_id'),
        Index('idx_ep_fname', 'first_name'),
    )
