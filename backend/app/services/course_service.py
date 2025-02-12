from typing import List, Optional, Dict, Any, Tuple
from sqlalchemy.orm import Session
from app.db.models import CourseDB, SchoolDB, PlatformDB
from app.db.repositories.course_repository import CourseRepository, SortField, SortOrder
import logging
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_, desc, and_
from sqlalchemy.orm import joinedload
from app.schemas.course import CourseListResponse, Course

logger = logging.getLogger(__name__)

class CourseService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = CourseRepository(db)
    
    async def get_paginated_courses(
        self,
        page: int = 0,
        limit: int = 10,
        engineer_level: Optional[str] = None,
        search_term: Optional[str] = None
    ) -> CourseListResponse:
        try:
            # Create base query with joins
            query = (
                select(CourseDB)
                .options(
                    joinedload(CourseDB.school),
                    joinedload(CourseDB.platform)
                )
            )
            
            # Apply filters
            filters = []
            if engineer_level:
                filters.append(CourseDB.engineer_level == engineer_level)
            if search_term:
                filters.append(CourseDB.title.ilike(f"%{search_term}%"))
            
            if filters:
                query = query.where(and_(*filters))
                
            # Get total count
            count_query = select(func.count()).select_from(query.subquery())
            total = await self.db.scalar(count_query) or 0
            
            # Apply pagination
            query = query.offset(page * limit).limit(limit)
            
            # Execute query
            result = await self.db.execute(query)
            courses = result.unique().scalars().all()
            
            # Convert to Pydantic models for validation
            validated_courses = []
            for course in courses:
                if course.school and course.platform:
                    try:
                        # Convert date to string if needed
                        if course.school.foundation_date:
                            course.school.foundation_date = course.school.foundation_date
                        validated_course = Course.model_validate(course)
                        validated_courses.append(validated_course)
                    except Exception as e:
                        logger.error(f"Error validating course {course.id}: {str(e)}")
                        continue
            
            return CourseListResponse(
                items=validated_courses,
                total=total,
                page=page,
                size=limit
            )
            
        except Exception as e:
            logger.error(f"Error in get_paginated_courses: {str(e)}")
            raise

    async def _get_filtered_courses(
        self,
        page: int,
        limit: int,
        engineer_level: Optional[str],
        min_price: Optional[float],
        max_price: Optional[float],
        categories: Optional[List[str]],
        school_id: Optional[int],
        platform_id: Optional[int],
        search_term: Optional[str],
        sort_by: Optional[str],
        sort_order: str
    ) -> Tuple[List[CourseDB], int]:
        query = (
            select(CourseDB)
            .options(
                joinedload(CourseDB.school),
                joinedload(CourseDB.platform)
            )
        )

        # Apply filters
        filters = []
        if engineer_level:
            filters.append(CourseDB.engineer_level == engineer_level)
        if min_price is not None:
            filters.append(CourseDB.price >= min_price)
        if max_price is not None:
            filters.append(CourseDB.price <= max_price)
        if categories:
            filters.append(CourseDB.categories.contains(categories))
        if school_id:
            filters.append(CourseDB.school_id == school_id)
        if platform_id:
            filters.append(CourseDB.platform_id == platform_id)
        if search_term:
            search_filter = or_(
                CourseDB.title.ilike(f"%{search_term}%"),
                CourseDB.description.ilike(f"%{search_term}%")
            )
            filters.append(search_filter)

        if filters:
            query = query.where(and_(*filters))

        # Apply sorting
        if sort_by and hasattr(CourseDB, sort_by):
            sort_column = getattr(CourseDB, sort_by)
            if sort_order == "desc":
                sort_column = desc(sort_column)
            query = query.order_by(sort_column)

        # Get total count
        count_query = select(func.count()).select_from(query.subquery())
        total = await self.db.scalar(count_query)

        # Apply pagination
        offset = page * limit
        query = query.offset(offset).limit(limit)

        # Execute query
        result = await self.db.execute(query)
        courses = result.unique().scalars().all()

        return courses, total

    async def get_course(self, course_id: int) -> Optional[CourseDB]:
        query = (
            select(CourseDB)
            .options(
                joinedload(CourseDB.school),
                joinedload(CourseDB.platform)
            )
            .filter(CourseDB.id == course_id)
        )
        result = await self.db.execute(query)
        return result.unique().scalar_one_or_none()
    
    def create_course(self, course: Course) -> CourseDB:
        return self.repository.create(course)
    
    def update_course(self, course_id: int, course: Course) -> Optional[CourseDB]:
        return self.repository.update(course_id, course)
    
    def delete_course(self, course_id: int) -> bool:
        return self.repository.delete(course_id)
    
    async def search_courses(
        self,
        search_term: str,
        page: int,
        size: int
    ) -> CourseListResponse:
        skip = (page - 1) * size
        query = self.db.query(CourseDB)
        
        if search_term:
            search = f"%{search_term}%"
            query = query.filter(
                or_(
                    CourseDB.title.ilike(search),
                    CourseDB.description.ilike(search)
                )
            )
        
        total = query.count()
        courses = query.offset(skip).limit(size).all()
        pages = (total + size - 1) // size
        
        return CourseListResponse(
            items=[Course.model_validate(course) for course in courses],
            total=total,
            page=page,
            size=size,
            pages=pages
        )
    
    def bulk_create(self, courses: List[Course]) -> List[Course]:
        return self.repository.bulk_create(courses)
    
    def bulk_delete(self, course_ids: List[int]) -> int:
        return self.repository.bulk_delete(course_ids)
    
    async def get_statistics(self) -> Dict[str, Any]:
        try:
            return await self.repository.get_statistics()
        except Exception as e:
            logger.error(f"Error creating statistics response: {str(e)}")
            return self.repository._get_default_statistics()

    async def get_courses(
        self,
        skip: int = 0,
        limit: int = 10,
        engineer_level: Optional[str] = None,
        search_term: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        categories: Optional[List[str]] = None,
        school_id: Optional[int] = None,
        platform_id: Optional[int] = None,
        sort_by: Optional[str] = None,
        sort_order: str = "asc"
    ) -> Dict[str, Any]:
        """Get paginated courses with filters"""
        # Create base query
        query = select(CourseDB)
        
        # Apply filters
        filters = []
        if engineer_level:
            filters.append(CourseDB.engineer_level == engineer_level)
        if min_price is not None:
            filters.append(CourseDB.price >= min_price)
        if max_price is not None:
            filters.append(CourseDB.price <= max_price)
        if categories:
            filters.append(CourseDB.categories.contains(categories))
        if school_id:
            filters.append(CourseDB.school_id == school_id)
        if platform_id:
            filters.append(CourseDB.platform_id == platform_id)
        if search_term:
            search_filter = or_(
                CourseDB.title.ilike(f"%{search_term}%"),
                CourseDB.description.ilike(f"%{search_term}%")
            )
            filters.append(search_filter)

        if filters:
            query = query.where(and_(*filters))

        # Apply sorting
        if sort_by and hasattr(CourseDB, sort_by):
            sort_column = getattr(CourseDB, sort_by)
            if sort_order == "desc":
                sort_column = desc(sort_column)
            query = query.order_by(sort_column)

        # Get total count
        count_query = select(func.count()).select_from(query.subquery())
        total = await self.db.scalar(count_query)

        # Apply pagination
        query = query.offset(skip).limit(limit)

        # Execute query
        result = await self.db.execute(query)
        courses = result.scalars().all()

        return {
            "items": courses,
            "total": total,
            "page": skip // limit + 1,
            "size": limit,
            "pages": (total + limit - 1) // limit
        } 