from pydantic import BaseModel, Field, HttpUrl
from datetime import date

class School(BaseModel):
    name: str = Field(..., description="Name of the school")
    address: HttpUrl = Field(..., description="URL of the school's website")
    logo: HttpUrl = Field(..., description="URL to the school's logo")
    foundation_date: date = Field(..., description="Date when the school was founded") 
    
    class Config:
        from_attributes = True  # This enables ORM mode