from fastapi import APIRouter,Depends
from database.db import get_db
from database.context import trace_id
from sqlalchemy.orm import Session
from schemas.user_schema import (UserRegister,UserLogin,UserRegistrationResponse,UserLoginResponse )
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

