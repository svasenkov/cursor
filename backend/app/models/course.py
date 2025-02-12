from enum import Enum
from sqlalchemy import Column, Integer, String
from app.db.base import Base

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

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    duration = Column(String)

# Remove CourseDB class from here since it's defined in app/db/models/course.py 