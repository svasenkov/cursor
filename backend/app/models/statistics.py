from pydantic import BaseModel, Field
from typing import Dict

class PriceStatistics(BaseModel):
    average: float = Field(ge=0)
    minimum: float = Field(ge=0)
    maximum: float = Field(ge=0)

class CourseStatistics(BaseModel):
    price: PriceStatistics
    engineer_levels: Dict[str, int] = Field(default_factory=dict)
    total_students: int = Field(ge=0)

    class Config:
        from_attributes = True 