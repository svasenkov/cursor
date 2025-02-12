from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.services.course_service import CourseService
from app.models.course import Course
from app.dependencies import get_course_service

router = APIRouter()

@router.get("/", response_model=List[Course])
async def get_courses(
    page: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    engineer_level: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    categories: Optional[List[str]] = Query(None),
    school_id: Optional[int] = None,
    platform_id: Optional[int] = None,
    search_term: Optional[str] = None,
    sort_by: Optional[str] = None,
    sort_order: Optional[str] = Query(default="asc", regex="^(asc|desc)$"),
    db: AsyncSession = Depends(get_db),
    course_service: CourseService = Depends(get_course_service)
):
    """
    Get list of courses with filtering and pagination
    """
    courses, total = await course_service.get_paginated_courses(
        page=page,
        limit=limit,
        engineer_level=engineer_level,
        min_price=min_price,
        max_price=max_price,
        categories=categories,
        school_id=school_id,
        platform_id=platform_id,
        search_term=search_term,
        sort_by=sort_by,
        sort_order=sort_order
    )
    
    return courses 