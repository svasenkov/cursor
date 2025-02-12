import json
from pathlib import Path
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models import CourseDB, SchoolDB, PlatformDB
from app.models.course import Course
from app.models.school import School
from app.models.platform import Platform
from datetime import datetime

def load_json(file_path: Path) -> dict:
    with open(file_path, 'r') as f:
        return json.load(f)

def parse_date(date_str: str) -> datetime.date:
    """Parse date string to date object"""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return None

async def migrate_schools(db, schools_data):
    for school_data in schools_data:
        school = SchoolDB(
            name=school_data["name"],
            address=school_data["address"],
            logo=school_data["logo"],
            foundation_date=parse_date(school_data["foundation_date"])
        )
        db.add(school)
    await db.commit()

def migrate_data():
    db = SessionLocal()
    try:
        # Load JSON data
        data_dir = Path(__file__).parent.parent / "data"
        schools_data = load_json(data_dir / "schools.json")
        platforms_data = load_json(data_dir / "platforms.json")
        courses_data = load_json(data_dir / "courses.json")

        # Clear existing data
        db.query(CourseDB).delete()
        db.query(PlatformDB).delete()
        db.query(SchoolDB).delete()
        db.commit()

        # Migrate schools
        await migrate_schools(db, schools_data["data"])

        # Migrate platforms
        for platform in platforms_data["data"]:
            existing_platform = db.query(PlatformDB).filter(PlatformDB.name == platform["name"]).first()
            if not existing_platform:
                db_platform = PlatformDB(
                    name=platform["name"],
                    url=platform["url"],
                    logo=platform["logo"],
                    description=platform["description"],
                    features=platform["features"]
                )
                db.add(db_platform)
        db.commit()

        # Migrate courses
        for course in courses_data["data"]:
            # Get related school and platform
            school = db.query(SchoolDB).filter(SchoolDB.name == course["school"]["name"]).first()
            platform = db.query(PlatformDB).filter(PlatformDB.name == course["platform"]["name"]).first()

            if school and platform:
                existing_course = db.query(CourseDB).filter(CourseDB.id == course["id"]).first()
                if not existing_course:
                    db_course = CourseDB(
                        id=course["id"],
                        title=course["title"],
                        description=course["description"],
                        instructor=course["instructor"],
                        duration=course["duration"],
                        price=course["price"],
                        school_id=school.id,
                        platform_id=platform.id,
                        categories=course["categories"],
                        engineer_level=course["engineer_level"],
                        students_amount=course["students_amount"],
                        rating=course["rating"]
                    )
                    db.add(db_course)
        db.commit()

        print("Data migration completed successfully!")

    except Exception as e:
        print(f"Error during migration: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    migrate_data() 