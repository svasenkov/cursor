from app.db.base_class import Base
from app.db.models.course import CourseDB
from app.db.models.school import SchoolDB
from app.db.models.platform import PlatformDB

# Re-export for convenience
__all__ = ['Base', 'CourseDB', 'SchoolDB', 'PlatformDB'] 