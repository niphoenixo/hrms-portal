# database/context.py
from contextvars import ContextVar
#from sqlalchemy.orm import Session
import uuid
# Create the storage variable
#db_session_context: ContextVar[Session] = ContextVar("db_session_context")
trace_id: ContextVar[str] = ContextVar("trace_id",default=str(uuid.uuid4()))