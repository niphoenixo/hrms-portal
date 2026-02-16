from fastapi import APIRouter,Request
from bulk.fake_data import fake_generate_company_data
from database.context import trace_id
router = APIRouter(
    prefix="/fake",
    tags=["fake company"]
)

@router.get("/company")
def fake_company_data(request:Request):
    filename= fake_generate_company_data()
    return {
        "message": "fake Companies data created", 
        "data": filename, 
        "trace_id": trace_id.get()
    }