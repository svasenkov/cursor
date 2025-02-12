from pydantic import BaseModel, Field, HttpUrl

class Platform(BaseModel):
    name: str = Field(..., description="Name of the platform")
    url: HttpUrl = Field(..., description="URL of the platform")
    logo: HttpUrl = Field(..., description="URL to the platform's logo")
    description: str = Field(..., min_length=10, max_length=1000, description="Platform description")
    features: list[str] = Field(
        default_factory=list,
        min_items=1,
        description="List of platform features"
    ) 

    class Config:
        from_attributes = True  # This enables ORM mode