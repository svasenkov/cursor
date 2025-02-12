from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class SchoolDB(Base):
    __tablename__ = "schools"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String)
    logo = Column(String)
    foundation_date = Column(Date)
    
    courses = relationship("CourseDB", back_populates="school")

    def __repr__(self):
        return f"<School {self.name}>" 