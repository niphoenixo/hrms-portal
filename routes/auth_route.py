from fastapi import APIRouter,Depends
from database.db import get_db
from database.context import trace_id
from sqlalchemy.orm import Session
from schemas.user_schema import (UserRegister,UserLogin,UserRegistrationResponse,UserLoginResponse )
from models.user_model import User

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/register",response_model=UserRegistrationResponse)
def register(body: UserRegister, db: Session = Depends(get_db)):
    user_data = body.model_dump()  
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
    return {
        "message": "Login", 
        "data": [], 
        "trace_id": trace_id.get()
    }
