from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from database.context import trace_id
import uuid

class AddTraceIDContext(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        header_id = request.headers.get("X-trace-id")
        invalid_ids = {None, "", "null", "none", '""'}
        if not header_id or not header_id.strip() or header_id.lower() in invalid_ids:
            request_id = str(uuid.uuid4())
        else:
            request_id = header_id

        tid = trace_id.set(request_id)
        request.state.trace_id = request_id
        request.state.created_by = request_id
        request.state.updated_by = request_id
        try:
            response = await call_next(request)
            response.headers["X-Trace-ID"] = request_id
            return response
        finally:
            trace_id.reset(tid)