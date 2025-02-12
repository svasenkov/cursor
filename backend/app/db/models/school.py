from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from .base import Base

class SchoolDB(Base):
    __tablename__ = "schools"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    address = Column(String)
    logo = Column(String)
    foundation_date = Column(Date)
    
    courses = relationship("CourseDB", back_populates="school") 