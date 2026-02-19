from sqlalchemy import Column, String, DateTime,ForeignKey
from sqlalchemy.dialects.mysql import BIGINT,TINYINT
from sqlalchemy.sql import func
from database.db import Base




class User(Base):
    __tablename__ = 'users'

    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    employee_id = Column(BIGINT(unsigned=True), nullable=False)
    user_name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    password = Column(String(255), nullable=False)
    is_active = Column(
        TINYINT, 
        nullable=False, 
        server_default='0', 
        comment='0 for inactive,1 for active ,2 for hold, 3 for deleted'
    )    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=None, onupdate=func.now())


class Role(Base):
    __tablename__ = 'roles'

    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    location_id = Column(BIGINT(unsigned=True), ForeignKey('locations.id'), nullable=False)
    role_name = Column(String(100), nullable=False)
    created_by = Column(String(36), nullable=False)
    updated_by = Column(String(36), nullable=False)
    is_active = Column(
        TINYINT, 
        nullable=False, 
        server_default='0', 
        comment='0 for inactive,1 for active ,2 for hold, 3 for deleted'
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class Permissions(Base):
    __tablename__ = 'permissions'

    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    module = Column(String(100), nullable=False)
    action = Column(String(50), nullable=False)
    created_by = Column(String(36), nullable=False)
    updated_by = Column(String(36), nullable=False)
    is_active = Column(
        TINYINT, 
        nullable=False, 
        server_default='0', 
        comment='0 for inactive,1 for active ,2 for hold, 3 for deleted'
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class RolePermissions(Base):
    __tablename__ = 'role_permissions'

    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    role_id = Column(BIGINT(unsigned=True), ForeignKey('roles.id'), nullable=False)
    permission_id = Column(BIGINT(unsigned=True), ForeignKey('permissions.id'), nullable=False)
    
class UserRoles(Base):
    __tablename__ = 'user_roles'

    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    role_id = Column(BIGINT(unsigned=True), ForeignKey('roles.id'), nullable=False)
    user_id = Column(BIGINT(unsigned=True), ForeignKey('users.id'), nullable=False)


class AuditLog(Base):
    __tablename__ = 'audit_logs'

    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    location_id = Column(BIGINT(unsigned=True), ForeignKey('locations.id'), nullable=False)
    user_id = Column(BIGINT(unsigned=True), ForeignKey('users.id'), nullable=False)
    action = Column(String(100),server_default=None,nullable=True)
    ip_address = Column(String(100),server_default=None,nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
