import jwt
from fastapi import APIRouter,Depends,Request
from database.db import get_db
from database.context import trace_id
from sqlalchemy.orm import Session
from schemas.user_schema import (UserRegister,UserLogin,UserRegistrationResponse,UserLoginResponse)
from schemas.generic_schema import GenericResponse

from models.user_model import User
from sqlalchemy import Select
from services.auth.auth_service import AuthService
from custom_response.json_response import CustomJSONResponse
from datetime import timedelta
from config.config import TOKEN_ALGORITHM,TOKEN_SECRET_KEY,TOKEN_EXPIRE_MINUTES

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/register",response_model=UserRegistrationResponse)
def register(body: UserRegister, db: Session = Depends(get_db)):
    user_data = body.model_dump()
    user_data['password']= AuthService.get_password_hash(body.password) 
    new_user = User(**user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user) 
    
    return {
        "message": "User Register", 
        "data": [new_user], 
        "trace_id": trace_id.get()
    }


@router.post("/login",response_model=UserLoginResponse)
def register(body:UserLogin,db:Session =Depends(get_db)):
    stmt = Select(User).where(User.email == body.email)
    user = db.scalars(stmt).first()
    if user:
        
        is_verify=AuthService.verify_password(body.password,user.password)
        if is_verify:
            access_token_expires = timedelta(minutes=TOKEN_EXPIRE_MINUTES)
            access_token = AuthService.create_token(
                data={"sub": user.email}, expires_delta=access_token_expires
            )
            data ={"id":user.id,"token":access_token}
            return CustomJSONResponse.success_json(data,"login")
        else:
             return CustomJSONResponse.error_json("password","Invalid Password")                                                                            
    else:
        return CustomJSONResponse.from_not_found("User")

    
@router.get("/verifytoken",response_model=UserRegistrationResponse)
def verify_token(request:Request,db:Session = Depends(get_db)):
    get_token=request.headers.get("authorization",None)
    invalid_ids = {None, "", "null", "none", '""'}
    if not get_token or not get_token.strip() or get_token.lower() in invalid_ids:
        return CustomJSONResponse.error_json("token","Invalid token")
        
    else:
        is_verify= AuthService.verify_token(get_token)
        if is_verify['status']==True:
            stmt = Select(User).where(User.email == is_verify["data"]["sub"])
            user = db.scalars(stmt).first()
            if user:
                return {
                    "message": is_verify["message"], 
                    "data": [user], 
                    "trace_id": trace_id.get()
                }
            else:
                return CustomJSONResponse.error_json("token","Unauthorized: Access is denied due to invalid user.",401)
        else:
            return CustomJSONResponse.error_json("token",is_verify["message"],401)

    