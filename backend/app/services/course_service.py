from typing import List, Optional, Dict, Any, Tuple
from sqlalchemy.orm import Session
from app.db.models import CourseDB
from app.models.course import Course
from app.models.pagination import PaginatedResponse
from app.db.repositories.course_repository import CourseRepository, SortField, SortOrder
from app.models.statistics import CourseStatistics, PriceStatistics
import logging
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_, desc, and_, any_, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import joinedload
from app.db.models import SchoolDB, PlatformDB

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
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        categories: Optional[List[str]] = None,
        school_id: Optional[int] = None,
        platform_id: Optional[int] = None,
        search_term: Optional[str] = None,
        sort_by: Optional[str] = None,
        sort_order: str = "asc"
    ) -> Tuple[List[CourseDB], int]:
        """Get paginated courses with filters"""
        try:
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
                # Split comma-separated categories into a list
                category_list = [cat.strip() for cat in categories[0].split(',')]
                filters.append(CourseDB.categories.contains(category_list))
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
            
        except Exception as e:
            logger.error(f"Error in get_paginated_courses: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error retrieving courses: {str(e)}"
            )
    
    async def get_course(self, course_id: int) -> Optional[Course]:
        try:
            course = await self.repository.get_course(course_id)
            if not course:
                raise HTTPException(status_code=404, detail="Course not found")
            return course
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error getting course {course_id}: {str(e)}")
            raise HTTPException(status_code=500, detail="Error retrieving course")
    
    def create_course(self, course: Course) -> Course:
        return self.repository.create(course)
    
    def update_course(self, course_id: int, course: Course) -> Optional[Course]:
        return self.repository.update(course_id, course)
    
    def delete_course(self, course_id: int) -> bool:
        return self.repository.delete(course_id)
    
    async def search_courses(
        self,
        search_term: str,
        page: int,
        size: int
    ) -> PaginatedResponse[Course]:
        skip = (page - 1) * size
        items = self.repository.search_courses(
            search_term=search_term,
            skip=skip,
            limit=size
        )
        total = len(items)  # For simplicity; in production, you'd want a separate count query
        pages = (total + size - 1) // size
        
        return PaginatedResponse[Course](
            items=items,
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
        filters: Dict[str, Any] = None
    ) -> Tuple[List[Course], int]:
        try:
            courses, total = await self.repository.get_filtered_courses(
                skip=skip,
                limit=limit,
                **filters if filters else {}
            )
            return courses, total
        except Exception as e:
            logger.error(f"Error getting courses: {str(e)}")
            raise HTTPException(status_code=500, detail="Error retrieving courses") 