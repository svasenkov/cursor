import asyncio
import json
from pathlib import Path
from app.db.database import engine
from app.models.course import Course
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

async def init_db():
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Course.metadata.create_all)

    # Load course data
    data_file = Path(__file__).parent.parent / "data" / "courses.json"
    with open(data_file) as f:
        courses_data = json.load(f)

    # Create async session
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        # Check if courses already exist
        result = await session.execute(Course.__table__.select())
        existing_courses = result.fetchall()
        
        if not existing_courses:
            # Add courses
            for course_data in courses_data["courses"]:
                course = Course(
                    title=course_data["title"],
                    description=course_data["description"],
                    duration=course_data["duration"]
                )
                session.add(course)
            
            await session.commit()

if __name__ == "__main__":
    asyncio.run(init_db()) 