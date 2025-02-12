from typing import List, Optional, Dict, Any, Tuple
from sqlalchemy import select, func, or_, desc, and_
from sqlalchemy.orm import joinedload
from fastapi_cache.decorator import cache
from datetime import timedelta
from app.core.config import get_settings
from app.db.repositories.base import BaseRepository
from app.db.models import CourseDB, SchoolDB, PlatformDB
from app.models.course import Course
from enum import Enum
import logging
from sqlalchemy.exc import SQLAlchemyError

settings = get_settings()
logger = logging.getLogger(__name__)

class SortField(str, Enum):
    PRICE = "price"
    RATING = "rating"
    STUDENTS = "students_amount"
    DATE = "created_at"
    TITLE = "title"

class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"

class CourseRepository(BaseRepository[CourseDB, Course, Course]):
    def __init__(self, db):
        super().__init__(CourseDB, db)
        
    async def get_filtered_courses(
        self,
        skip: int = 0,
        limit: int = 10,
        engineer_level: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        categories: Optional[List[str]] = None,
        school_id: Optional[int] = None,
        platform_id: Optional[int] = None,
        sort_by: Optional[SortField] = None,
        sort_order: SortOrder = SortOrder.ASC,
        search_term: Optional[str] = None
    ) -> Tuple[List[CourseDB], int]:
        """
        Get filtered courses with pagination and total count
        Returns tuple of (courses, total_count)
        """
        try:
            # Base query with joins
            query = (
                select(CourseDB)
                .options(
                    joinedload(CourseDB.school),
                    joinedload(CourseDB.platform)
                )
            )

            # Build filter conditions
            conditions = []
            if engineer_level:
                conditions.append(CourseDB.engineer_level == engineer_level)
            if min_price is not None:
                conditions.append(CourseDB.price >= min_price)
            if max_price is not None:
                conditions.append(CourseDB.price <= max_price)
            if categories:
                conditions.append(CourseDB.categories.overlap(categories))
            if school_id:
                conditions.append(CourseDB.school_id == school_id)
            if platform_id:
                conditions.append(CourseDB.platform_id == platform_id)
            if search_term:
                search_filter = or_(
                    CourseDB.title.ilike(f"%{search_term}%"),
                    CourseDB.description.ilike(f"%{search_term}%"),
                    CourseDB.instructor.ilike(f"%{search_term}%")
                )
                conditions.append(search_filter)

            # Apply all filters
            if conditions:
                query = query.where(and_(*conditions))

            # Get total count before pagination
            count_query = select(func.count()).select_from(query.subquery())
            total = await self.db.scalar(count_query)

            # Apply sorting
            if sort_by:
                order_column = getattr(CourseDB, sort_by.value)
                if sort_order == SortOrder.DESC:
                    order_column = desc(order_column)
                query = query.order_by(order_column)
            
            # Apply pagination
            query = query.offset(skip).limit(limit)
            
            # Execute query
            result = await self.db.execute(query)
            courses = result.unique().scalars().all()
            
            return courses, total

        except SQLAlchemyError as e:
            logger.error(f"Database error in get_filtered_courses: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in get_filtered_courses: {str(e)}")
            raise

    @cache(expire=timedelta(seconds=settings.CACHE_EXPIRATION_SECONDS))
    async def get_statistics(self) -> Dict[str, Any]:
        """Get course statistics with caching"""
        try:
            # Price statistics
            price_stats = await self.db.execute(
                select(
                    func.avg(CourseDB.price).label('avg_price'),
                    func.min(CourseDB.price).label('min_price'),
                    func.max(CourseDB.price).label('max_price'),
                    func.percentile_cont(0.5).within_group(
                        CourseDB.price.asc()
                    ).label('median_price')
                )
            )
            price_stats = price_stats.first()._asdict()  # Convert to dict

            # Level distribution
            level_counts = await self.db.execute(
                select(
                    CourseDB.engineer_level,
                    func.count(CourseDB.id).label('count')
                )
                .group_by(CourseDB.engineer_level)
                .having(CourseDB.engineer_level.isnot(None))
            )
            level_counts = {level: count for level, count in level_counts.fetchall()}

            # Category distribution
            category_stats = await self.db.execute(
                select(
                    func.unnest(CourseDB.categories).label('category'),
                    func.count().label('count')
                )
                .group_by('category')
            )
            category_stats = {cat: count for cat, count in category_stats.fetchall()}

            # Platform distribution
            platform_stats = await self.db.execute(
                select(
                    PlatformDB.name,
                    func.count(CourseDB.id).label('count')
                )
                .join(CourseDB)
                .group_by(PlatformDB.name)
            )
            platform_stats = {name: count for name, count in platform_stats.fetchall()}

            return {
                'price_statistics': {
                    'average': round(float(price_stats.get('avg_price') or 0), 2),
                    'median': round(float(price_stats.get('median_price') or 0), 2),
                    'minimum': round(float(price_stats.get('min_price') or 0), 2),
                    'maximum': round(float(price_stats.get('max_price') or 0), 2)
                },
                'level_distribution': level_counts,
                'category_distribution': category_stats,
                'platform_distribution': platform_stats
            }

        except SQLAlchemyError as e:
            logger.error(f"Database error in get_statistics: {str(e)}")
            return self._get_default_statistics()
        except Exception as e:
            logger.error(f"Unexpected error in get_statistics: {str(e)}")
            return self._get_default_statistics()

    def _get_default_statistics(self) -> Dict[str, Any]:
        """Return default statistics in case of error"""
        return {
            'price_statistics': {
                'average': 0.0,
                'median': 0.0,
                'minimum': 0.0,
                'maximum': 0.0
            },
            'level_distribution': {},
            'category_distribution': {},
            'platform_distribution': {}
        }

    def get_total_count(
        self,
        engineer_level: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None
    ) -> int:
        query = select(func.count()).select_from(CourseDB)
        
        if engineer_level:
            query = query.where(CourseDB.engineer_level == engineer_level)
        if min_price is not None:
            query = query.where(CourseDB.price >= min_price)
        if max_price is not None:
            query = query.where(CourseDB.price <= max_price)
            
        result = self.db.execute(query)
        return result.scalar()

    @cache(expire=timedelta(seconds=settings.CACHE_EXPIRATION_SECONDS))
    async def get_course(self, course_id: int) -> Optional[Course]:
        return super().get(course_id)

    def search_courses(
        self,
        search_term: str,
        skip: int = 0,
        limit: int = 10
    ) -> List[CourseDB]:
        query = select(CourseDB).where(
            or_(
                CourseDB.title.ilike(f"%{search_term}%"),
                CourseDB.description.ilike(f"%{search_term}%"),
                CourseDB.instructor.ilike(f"%{search_term}%")
            )
        )
        query = query.offset(skip).limit(limit)
        result = self.db.execute(query)
        return list(result.scalars().all())

    def bulk_create(self, courses: List[Course]) -> List[Course]:
        db_courses = [CourseDB(**course.model_dump()) for course in courses]
        self.db.add_all(db_courses)
        self.db.commit()
        for db_course in db_courses:
            self.db.refresh(db_course)
        return db_courses

    def bulk_delete(self, course_ids: List[int]) -> int:
        result = self.db.execute(
            CourseDB.__table__.delete().where(CourseDB.id.in_(course_ids))
        )
        self.db.commit()
        return result.rowcount 