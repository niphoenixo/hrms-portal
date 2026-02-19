from typing import List, TypeVar, Generic
from pydantic import BaseModel

T = TypeVar("T")

class GenericResponse(BaseModel, Generic[T]):
    message: str
    trace_id: str
    data: List[T]  # This will adapt to whatever class you pass in
