from typing import TypeVar, Generic, List
from pydantic import BaseModel, ConfigDict

T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int
    pages: int

    model_config = ConfigDict(arbitrary_types_allowed=True) 