from sqlalchemy import Column, Integer, String, Float, ForeignKey, ARRAY
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class CourseDB(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False, server_default='')
    instructor = Column(String, nullable=False, server_default='')
    duration = Column(String, nullable=False, server_default='')
    price = Column(Float, nullable=False, server_default='0')
    school_id = Column(Integer, ForeignKey('schools.id', ondelete='CASCADE'), nullable=False)
    platform_id = Column(Integer, ForeignKey('platforms.id', ondelete='CASCADE'), nullable=False)
    categories = Column(ARRAY(String), nullable=False, server_default='{}')
    engineer_level = Column(String, nullable=False, server_default='')
    students_amount = Column(Integer, nullable=False, server_default='0')
    rating = Column(Float, nullable=False, server_default='0')

    school = relationship("SchoolDB", back_populates="courses")
    platform = relationship("PlatformDB", back_populates="courses")

    def __repr__(self):
        return f"<Course {self.title}>"

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