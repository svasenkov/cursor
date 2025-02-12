from sqlalchemy import Column, Integer, String, Float, ForeignKey, ARRAY
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from .base import Base

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

    def to_dict(self):
        """Convert model instance to dictionary"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "instructor": self.instructor,
            "duration": self.duration,
            "price": self.price,
            "engineer_level": self.engineer_level,
            "students_amount": self.students_amount,
            "rating": self.rating,
            "categories": self.categories,
            "school_id": self.school_id,
            "platform_id": self.platform_id
        } 