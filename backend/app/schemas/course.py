from typing import List, Optional
from pydantic import BaseModel, ConfigDict, validator, field_validator
from datetime import datetime, date

class SchoolBase(BaseModel):
    id: int
    name: str
    address: Optional[str] = None
    logo: Optional[str] = None
    foundation_date: Optional[date] = None

    model_config = ConfigDict(from_attributes=True)

    @field_validator('foundation_date', mode='before')
    @classmethod
    def parse_date(cls, value):
        if isinstance(value, str):
            return date.fromisoformat(value)
        return value

class PlatformBase(BaseModel):
    id: int
    name: str
    url: Optional[str] = None
    logo: Optional[str] = None
    description: Optional[str] = None
    features: List[str] = []

    model_config = ConfigDict(from_attributes=True)

class CourseBase(BaseModel):
    id: int
    title: str
    description: str = ""
    instructor: str = ""
    duration: str = ""
    price: float = 0.0
    school_id: int
    platform_id: int
    categories: List[str] = []
    engineer_level: str = ""
    students_amount: int = 0
    rating: float = 0.0

    @validator('categories')
    def validate_categories(cls, v):
        if not v:
            raise ValueError("At least one category is required")
        if len(set(v)) != len(v):
            raise ValueError("Categories must be unique")
        return v

    @validator('rating')
    def validate_rating(cls, v):
        if v < 0 or v > 5:
            raise ValueError('Rating must be between 0 and 5')
        return v

    model_config = ConfigDict(from_attributes=True)

class CourseCreate(CourseBase):
    school_id: int

class CourseUpdate(CourseBase):
    title: Optional[str] = None
    description: Optional[str] = None
    instructor: Optional[str] = None
    duration: Optional[str] = None
    price: Optional[float] = None
    categories: Optional[List[str]] = None
    engineer_level: Optional[str] = None
    students_amount: Optional[int] = None
    rating: Optional[float] = None
    school_id: Optional[int] = None

class Course(CourseBase):
    school: SchoolBase
    platform: PlatformBase

    model_config = ConfigDict(from_attributes=True)

class CourseListResponse(BaseModel):
    items: List[Course]
    total: int
    page: int = 0
    size: int = 10

    model_config = ConfigDict(from_attributes=True)

class CourseResponse(BaseModel):
    id: int
    title: str
    description: str
    duration: str

    class Config:
        from_attributes = True 