from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.services.course_service import CourseService

async def get_course_service(db: AsyncSession = Depends(get_db)) -> CourseService:
    return CourseService(db) 