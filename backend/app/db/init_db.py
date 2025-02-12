import json
import asyncio
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import async_session_maker
from app.db.models import SchoolDB, PlatformDB, CourseDB
from app.core.config import get_settings

settings = get_settings()

async def init_db():
    """Initialize database with sample data"""
    try:
        # Load data from JSON file
        data_file = Path(__file__).parent.parent / 'data' / 'courses.json'
        with open(data_file, 'r') as f:
            data = json.load(f)

        async with async_session_maker() as session:
            # Clear existing data
            await session.execute(CourseDB.__table__.delete())
            await session.execute(SchoolDB.__table__.delete())
            await session.execute(PlatformDB.__table__.delete())
            
            # Insert schools
            schools = []
            for school_data in data['schools']:
                school = SchoolDB(**school_data)
                schools.append(school)
                session.add(school)
            await session.flush()

            # Insert platforms
            platforms = []
            for platform_data in data['platforms']:
                platform = PlatformDB(**platform_data)
                platforms.append(platform)
                session.add(platform)
            await session.flush()

            # Insert courses
            for course_data in data['courses']:
                course = CourseDB(**course_data)
                session.add(course)

            await session.commit()

        print("Database initialized successfully!")
        
    except Exception as e:
        print(f"Error initializing database: {str(e)}")
        raise

async def main():
    """Main function to run database initialization"""
    await init_db()

if __name__ == "__main__":
    asyncio.run(main()) 