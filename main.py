import os
from fastapi import FastAPI,Depends,HTTPException,Request
from dotenv import load_dotenv
from database.db import get_db,engine,Base
from sqlalchemy.orm import Session
from config import config
from routes import (company_route,location_route,fake_route,bulk_data_route,auth_route)
from middleware.trace_id_middleware import AddTraceIDContext
#custom error
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from database.context import trace_id
from custom_response.json_response import CustomJSONResponse
# Load environment variables
load_dotenv()

# Create the database tables 
# (Note: In production, you'd use Alembic for this)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="HRMS PORTAL")
#custom error
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return CustomJSONResponse(
        status_code=422, 
        message="Request validation failed"
    ).from_pydantic_error(exc)
    
#add middleware
app.add_middleware(AddTraceIDContext)

#add routes
app.include_router(company_route.router)
app.include_router(location_route.router)
app.include_router(auth_route.router)
#fake data create
app.include_router(fake_route.router)
#bulk upload 
app.include_router(bulk_data_route.router)
@app.get("/")
def root():
    return {
        "message": "Welcome to the HRMS API",
        "status": "Online",
        "docs": "/docs",
        "db":"db"
    }

# @app.get("/db-check")
# def check_connection(db: Session = Depends(get_db)):
#     try:
#         # Simple query to check if the DB is responding
#         from sqlalchemy import text
#         db.execute(text("SELECT 1"))
#         return {"status": "Database connection is healthy"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")
#pip install cryptography mysql-connector-python  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
# # Example Route for Employees (Placeholder)
# @app.get("/employees")
# def get_employees(db: Session = Depends(get_db)):
#     # This is where you would query your Employee model later
#     return {"data": []}