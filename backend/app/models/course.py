from pydantic import BaseModel, Field, validator
from enum import Enum
from typing import List
from app.models.school import School
from app.models.platform import Platform

class EngineerLevel(str, Enum):
    NEW = "new"
    JUNIOR = "junior"
    MIDDLE = "middle"
    SENIOR = "senior"
    HEAD = "head"

class SchoolName(str, Enum):
    QA_GURU = "qa.guru"
    LEARN_QA = "learnqa.ru"
    SOFTWARE_TESTING = "software-testing.ru"
    QA_COUNTRY_ROAD = "t.me/qa_country_road"
    CHURSOV_QA = "t.me/chursovQA"

class Course(BaseModel):
    id: int = Field(..., gt=0, description="Unique course identifier")
    title: str = Field(..., min_length=3, max_length=100, description="Course title")
    description: str = Field(..., min_length=10, max_length=1000, description="Course description")
    instructor: str = Field(..., min_length=2, max_length=100, description="Course instructor name")
    duration: str = Field(..., pattern="^[0-9]+ (days|weeks|months)$", description="Course duration (e.g., '8 weeks')")
    price: float = Field(..., ge=0, description="Course price")
    school: School = Field(..., description="School providing the course")
    platform: Platform = Field(..., description="Platform hosting the course")
    categories: List[str] = Field(
        default_factory=list,
        min_items=1,
        max_items=10,
        description="List of course categories"
    )
    engineer_level: EngineerLevel = Field(
        default=EngineerLevel.NEW,
        description="Target engineer level for the course"
    )
    students_amount: int = Field(
        default=0,
        ge=0,
        description="Number of enrolled students"
    )
    rating: float = Field(
        default=0.0,
        ge=0.0,
        le=10.0,
        description="Course rating from 0 to 10"
    )

    @validator('categories')
    def validate_categories(cls, v):
        if not v:
            raise ValueError("At least one category is required")
        if len(set(v)) != len(v):
            raise ValueError("Categories must be unique")
        return v

    class Config:
        from_attributes = True  # This enables ORM mode
    