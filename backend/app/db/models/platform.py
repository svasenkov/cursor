from sqlalchemy import Column, Integer, String, ARRAY
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class PlatformDB(Base):
    __tablename__ = "platforms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    url = Column(String)
    logo = Column(String)
    description = Column(String)
    features = Column(ARRAY(String))

    courses = relationship("CourseDB", back_populates="platform") 