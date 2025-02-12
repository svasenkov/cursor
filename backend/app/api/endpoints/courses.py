from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
from app.schemas.course import Course, CourseListResponse, CourseResponse
from app.services.course_service import CourseService
import logging
from app.db.database import get_session
from app.models.course import Course as DBCourse
from typing import List

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/{course_id}", response_model=Course)
async def get_course(
    course_id: int, 
    db: AsyncSession = Depends(get_db)
):
    course_service = CourseService(db)
    course = await course_service.get_course(course_id)
    if course is None:
        raise HTTPException(
            status_code=404,
            detail=f"Course with id {course_id} not found"
        )
    return course

@router.get("/", response_model=CourseListResponse)
async def get_courses(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0, alias="page"),
    limit: int = Query(10, ge=1, le=100),
    engineer_level: str | None = None,
    search_term: str | None = None
):
    try:
        course_service = CourseService(db)
        result = await course_service.get_paginated_courses(
            page=skip,
            limit=limit,
            engineer_level=engineer_level,
            search_term=search_term
        )
        return result
    except Exception as e:
        logger.error(f"Error in get_courses endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error while retrieving courses"
        )

@router.get("/courses", response_model=List[CourseResponse])
async def get_courses_from_db(session: AsyncSession = Depends(get_session)):
    result = await session.execute(DBCourse.__table__.select())
    courses = result.fetchall()
    return [
        {
            "id": course.id,
            "title": course.title,
            "description": course.description,
            "duration": course.duration
        }
        for course in courses
    ] 