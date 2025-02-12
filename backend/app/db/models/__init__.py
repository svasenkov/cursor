from app.db.base_class import Base
from .school import SchoolDB
from .platform import PlatformDB
from .course import CourseDB

__all__ = ['Base', 'SchoolDB', 'PlatformDB', 'CourseDB'] 