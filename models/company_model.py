from sqlalchemy import Column, String, DateTime, Index,ForeignKey
from sqlalchemy.dialects.mysql import BIGINT, TINYINT, MEDIUMTEXT, JSON,TEXT
from sqlalchemy.sql import func
from database.db import Base


class Company(Base):
    __tablename__ = 'companies'

    id = Column(
        BIGINT(unsigned=True), 
        primary_key=True, 
        autoincrement=True, 
        nullable=False
    )
    company_uuid = Column(String(36), nullable=False)
    company_name = Column(String(100), nullable=False)
    
    company_registration_no = Column(
        String(100), 
        nullable=False, 
        unique=True,
        comment='company registration no'
    )
    
    company_type = Column(
        String(100), 
        nullable=False, 
        server_default='private', 
        comment='company type like private,public,ngo,govt etc'
    )
    
    company_type_meta = Column(
        String(100), 
        nullable=False, 
        comment='company like software,manufacturing,education etc'
    )
    
    company_web = Column(MEDIUMTEXT, nullable=True)
    
    company_logo = Column(String(255), nullable=True, comment='company logo image')
    company_email = Column(String(255), nullable=False, comment='company email')
    company_contact_no = Column(String(255), nullable=False, comment='company contact no')
    company_country = Column(String(50), nullable=True, comment='company country')

    company_gst_no = Column(String(255), nullable=True)
    company_pan_no = Column(String(255), nullable=False)
    company_tin_no = Column(String(255), nullable=False)
    company_cin_no = Column(String(255), nullable=False)
    
    company_meta = Column(JSON, nullable=True, comment='json detail for other info')
    
    created_by = Column(String(36), nullable=False)
    updated_by = Column(String(36), nullable=False)
    
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    
    is_active = Column(
        TINYINT, 
        nullable=False, 
        server_default='0', 
        comment='0 for inactive,1 for active ,2 for hold, 3 for deleted'
    )

    # Indexes
    __table_args__ = (
        Index('company_company_name_company_uuid_index', 'company_name', 'company_uuid'),
        Index('company_id_index', 'id'),
    )


class CompanyDepartment(Base):
    __tablename__ = 'company_department'

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
        comment='company table id'
    )
    
    department_uuid = Column(String(36), nullable=False)
    
    department_name = Column(
        String(50), 
        nullable=False, 
        comment='department name like HR,PAYROLL etc'
    )
    
    created_by = Column(String(36), nullable=False)
    updated_by = Column(String(36), nullable=False)
    
    is_active_department = Column(
        TINYINT, 
        nullable=False, 
        server_default='0', 
        comment='0 for inactive,1 for active ,2 for hold, 3 for deleted'
    )
    
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index('company_department_company_id_index', 'company_id'),
        Index('company_department_department_uuid_index', 'department_uuid'),
        Index('company_department_department_name_index', 'department_name'),
    )

class CompanyWorkType(Base):
    __tablename__ = 'company_work_type'
    id = Column(BIGINT(unsigned=True), primary_key=True)
    work_type_uuid = Column(String(36), nullable=False)
    company_id = Column(BIGINT(unsigned=True), ForeignKey('companies.id'), nullable=False)
    work_type = Column(String(25), nullable=False, comment='remote, hybrid, onsite')
    is_active = Column(TINYINT, server_default='0', nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    created_by = Column(String(36), nullable=False)
    updated_by = Column(String(36), nullable=False)
    __table_args__ = (Index('idx_work_type_comp_uuid', 'company_id', 'work_type_uuid'),)

class CompanyJobType(Base):
    __tablename__ = 'company_job_type'
    id = Column(BIGINT(unsigned=True), primary_key=True)
    job_type_uuid = Column(String(36), nullable=False)
    company_id = Column(BIGINT(unsigned=True), ForeignKey('companies.id'), nullable=False)
    job_type = Column(String(25), nullable=False, comment='full time, part time')
    is_active = Column(TINYINT, server_default='0', nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    created_by = Column(String(36), nullable=False)
    updated_by = Column(String(36), nullable=False)
    __table_args__ = (Index('idx_job_type_comp_uuid', 'company_id', 'job_type_uuid'),)

# 6. Company Actions
class CompanyAction(Base):
    __tablename__ = 'company_action'
    id = Column(BIGINT(unsigned=True), primary_key=True)
    action_uuid = Column(String(36), nullable=False)
    company_id = Column(BIGINT(unsigned=True))
    action_name = Column(String(25), nullable=False)
    is_active = Column(TINYINT, server_default='0', nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    created_by = Column(String(36), nullable=False)
    updated_by = Column(String(36), nullable=False)
    __table_args__ = (Index('idx_action_comp_uuid', 'company_id', 'action_uuid'),)

class CompanyEmpAction(Base):
    __tablename__ = 'company_emp_action'
    id = Column(BIGINT(unsigned=True), primary_key=True)
    company_id = Column(BIGINT(unsigned=True), ForeignKey('companies.id'), nullable=False)
    location_id = Column(BIGINT(unsigned=True), ForeignKey('locations.id'), nullable=False)
    company_action_id = Column(BIGINT(unsigned=True), ForeignKey('company_action.id'), nullable=False)
    emp_id = Column(BIGINT(unsigned=True), ForeignKey('employee.id'), nullable=False)
    is_active_shift_location = Column(TINYINT, server_default='0', nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    created_by = Column(String(36), nullable=False)
    updated_by = Column(String(36), nullable=False)

# Company Location Department (Mapping Table)
class CompanyLocationDepartment(Base):
    __tablename__ = 'company_location_department'

    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    company_id = Column(BIGINT(unsigned=True), ForeignKey('companies.id'), nullable=False)
    location_id = Column(BIGINT(unsigned=True), ForeignKey('locations.id'), nullable=False)
    department_id = Column(BIGINT(unsigned=True), ForeignKey('company_department.id'), nullable=False)
    
    created_by = Column(String(36), nullable=False)
    updated_by = Column(String(36), nullable=False)
    is_active_location_department = Column(TINYINT, server_default='0', nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    __table_args__ = (
        Index('idx_cld_company', 'company_id'),
        Index('idx_cld_location', 'location_id'),
        Index('idx_cld_department', 'department_id'),
    )

# 2. Company Designation
class CompanyDesignation(Base):
    __tablename__ = 'company_designation'

    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    company_id = Column(BIGINT(unsigned=True), ForeignKey('companies.id'), nullable=False)
    designation_uuid = Column(String(36), nullable=False)
    designation_name = Column(String(50), nullable=False, comment='HR, PAYROLL etc')
    designation_level = Column(String(50), nullable=False)
    
    created_by = Column(String(36), nullable=False)
    updated_by = Column(String(36), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    __table_args__ = (
        Index('idx_cd_company', 'company_id'),
        Index('idx_cd_uuid', 'designation_uuid'),
        Index('idx_cd_name', 'designation_name'),
    )
