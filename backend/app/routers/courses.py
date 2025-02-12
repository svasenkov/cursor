from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.services.course_service import CourseService
from app.dependencies import get_course_service
from app.models.course import Course
from app.models.pagination import PaginatedResponse
from app.models.statistics import CourseStatistics
from app.db.repositories.course_repository import SortField, SortOrder

router = APIRouter(prefix="/courses", tags=["courses"])

@router.get("/statistics")
async def get_statistics(
    service: CourseService = Depends(get_course_service)
):
    return await service.get_statistics()

@router.get("/", response_model=List[Course])
async def get_courses(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    service: CourseService = Depends(get_course_service)
):
    courses, _ = await service.get_courses(skip=skip, limit=limit)
    return courses

@router.get("/{course_id}", response_model=Course)
async def get_course(
    course_id: int,
    service: CourseService = Depends(get_course_service)
):
    return await service.get_course(course_id)

@router.get("/statistics", response_model=CourseStatistics)
async def get_course_statistics(
    course_service: CourseService = Depends(get_course_service)
) -> CourseStatistics:
    """Get course statistics"""
    try:
        return course_service.get_statistics()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Error retrieving statistics"
        )

@router.get("/search", response_model=PaginatedResponse[Course])
async def search_courses(
    q: str = Query(..., min_length=3, description="Search term"),
    page: int = Query(default=1, ge=1),
    size: int = Query(default=10, ge=1, le=100),
    course_service: CourseService = Depends(get_course_service)
) -> PaginatedResponse[Course]:
    """Search courses by title, description, or instructor"""
    return await course_service.search_courses(q, page, size)

@router.post("", response_model=Course)
async def create_course(
    course: Course,
    course_service: CourseService = Depends(get_course_service)
):
    """Create a new course"""
    return course_service.create_course(course)

@router.put("/{course_id}", response_model=Course)
async def update_course(
    course_id: int,
    course: Course,
    course_service: CourseService = Depends(get_course_service)
):
    """Update an existing course"""
    updated_course = course_service.update_course(course_id, course)
    if updated_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return updated_course

@router.delete("/{course_id}")
async def delete_course(
    course_id: int,
    course_service: CourseService = Depends(get_course_service)
):
    """Delete a course"""
    if not course_service.delete_course(course_id):
        raise HTTPException(status_code=404, detail="Course not found")
    return {"message": "Course deleted successfully"}

@router.post("/bulk", response_model=List[Course])
async def bulk_create_courses(
    courses: List[Course],
    course_service: CourseService = Depends(get_course_service)
):
    """Create multiple courses at once"""
    return course_service.bulk_create(courses)

@router.delete("/bulk")
async def bulk_delete_courses(
    course_ids: List[int],
    course_service: CourseService = Depends(get_course_service)
):
    """Delete multiple courses at once"""
    deleted_count = course_service.bulk_delete(course_ids)
    return {"deleted_count": deleted_count}

# ... Add other course-related endpoints here 