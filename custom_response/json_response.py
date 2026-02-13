from fastapi.responses import JSONResponse
from database.context import trace_id

class CustomJSONResponse:

    def __init__(self, status_code=400, message="Validation failed", custom_details=None):
        self.status_code = status_code
        self.message = message
        self.trace_id = trace_id.get()
        self.custom_details = custom_details or []

    def to_json(self, error_details=None):
        details = error_details if error_details is not None else self.custom_details
        return JSONResponse(
            status_code=self.status_code,
            content={
                "message": self.message,
                "trace_id": self.trace_id,
                "detail": details
            },
        )

    def from_pydantic_error(self, e):
        errors = e.errors()
        formatted_details = [
            {
                "field": err.get("loc")[-1],
                "message": err.get("msg")
            }
            for err in errors
        ]  
        
        return self.to_json(error_details=formatted_details)
    
    @classmethod
    def from_server_error(cls, e: Exception,message="Internal Server Error"):
        return cls(
            status_code=500, 
            message=message
        ).to_json(error_details=[{"field": "server", "message": "An unexpected error occurred."}])
    

    @classmethod
    def from_not_found(cls, resource_name="Resource"):
        return cls(
            status_code=404,
            message=f"{resource_name} not found"
        ).to_json(error_details=[{
            "field": resource_name.lower().replace(" ", "_"), 
            "message": f"The requested {resource_name} does not exist."
        }])