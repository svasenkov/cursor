from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
from app.schemas.course import Course, CourseListResponse
from app.services.course_service import CourseService
from fastapi_cache.decorator import cache
import logging

logger = logging.getLogger(__name__)
router = APIRouter(redirect_slashes=True)

@router.get("/statistics", tags=["statistics"])
@cache(expire=300)  # Cache for 5 minutes
async def get_course_statistics(
    db: AsyncSession = Depends(get_db)
):
    """
    Get course statistics including:
    - Total number of courses
    - Average rating
    - Most popular categories
    - Distribution by engineer level
    """
    try:
        course_service = CourseService(db)
        return await course_service.get_statistics()
    except Exception as e:
        logger.error(f"Error getting course statistics: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error retrieving course statistics"
        )

@router.get("", response_model=CourseListResponse)
async def get_courses(
    db: AsyncSession = Depends(get_db),
    page: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    engineer_level: str | None = None,
    search_term: str | None = None
):
    try:
        course_service = CourseService(db)
        result = await course_service.get_paginated_courses(
            page=page,
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