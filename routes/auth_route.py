from fastapi import APIRouter,Depends
from database.db import get_db
from database.context import trace_id
from sqlalchemy.orm import Session
from schemas.user_schema import (UserRegister,UserLogin)
from models.user_model import User

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/register")
def register(body: UserRegister, db: Session = Depends(get_db)):
    user_data = body.model_dump()  
    new_user = User(**user_data)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user) 
    
    return {
        "body": new_user, 
        "trace_id": trace_id.get()
    }


@router.post("/login")
def register(body:UserLogin,db:Session =Depends(get_db)):
    return {"body":body,"trace_id":trace_id.get()}
