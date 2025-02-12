from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, ARRAY
from sqlalchemy.orm import relationship
from .database import Base

class CourseDB(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    instructor = Column(String)
    duration = Column(String)
    price = Column(Float)
    school_id = Column(Integer, ForeignKey('schools.id'))
    platform_id = Column(Integer, ForeignKey('platforms.id'))
    categories = Column(ARRAY(String))
    engineer_level = Column(String)
    students_amount = Column(Integer)
    rating = Column(Float)

    school = relationship("SchoolDB", back_populates="courses")
    platform = relationship("PlatformDB", back_populates="courses")

class SchoolDB(Base):
    __tablename__ = "schools"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    address = Column(String)
    logo = Column(String)
    foundation_date = Column(Date)
    
    courses = relationship("CourseDB", back_populates="school")

class PlatformDB(Base):
    __tablename__ = "platforms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    url = Column(String)
    logo = Column(String)
    description = Column(String)
    features = Column(ARRAY(String))

    courses = relationship("CourseDB", back_populates="platform") 