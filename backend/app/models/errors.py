from pydantic import BaseModel
from typing import Optional, Any

class ErrorResponse(BaseModel):
    detail: str
    error_code: str
    metadata: Optional[dict[str, Any]] = None

class ValidationError(BaseModel):
    field: str
    message: str 