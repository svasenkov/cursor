import json
from pathlib import Path
from app.db.database import SessionLocal
from app.db.models.course import CourseDB
from app.db.models.school import SchoolDB
from app.db.models.platform import PlatformDB

def init_db() -> None:
    db = SessionLocal()
    
    try:
        # Check if we already have data
        if db.query(CourseDB).first():
            return

        # Load data from JSON file
        data_file = Path(__file__).parent.parent / "data" / "courses.json"
        with open(data_file) as f:
            data = json.load(f)

        # Create schools first
        schools = {}
        for school_data in data["schools"]:
            school = SchoolDB(**school_data)
            db.add(school)
            schools[school.name] = school

        # Create platforms
        platforms = {}
        for platform_data in data["platforms"]:
            platform = PlatformDB(**platform_data)
            db.add(platform)
            platforms[platform.name] = platform

        db.commit()

        # Create courses
        for course_data in data["courses"]:
            course = CourseDB(**course_data)
            db.add(course)

        db.commit()
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_db() 