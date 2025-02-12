from typing import List
from pydantic import BaseModel

class CourseBase(BaseModel):
    id: int
    title: str
    description: str
    instructor: str
    duration: str
    price: float
    engineer_level: str
    students_amount: int
    rating: float
    categories: List[str]

    class Config:
        from_attributes = True

class CourseListResponse(BaseModel):
    items: List[CourseBase]
    total: int 