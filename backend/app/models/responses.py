from pydantic import BaseModel
from typing import Generic, TypeVar, List, Dict, Any

T = TypeVar('T')

class SuccessResponse(BaseModel):
    message: str

class ErrorDetail(BaseModel):
    field: str
    message: str

class ErrorResponse(BaseModel):
    detail: str
    error_code: str
    metadata: Dict[str, Any] = None

class BulkResponse(BaseModel):
    deleted_count: int 