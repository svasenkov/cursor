from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.db.models import SchoolDB
from sqlalchemy import select
from fastapi_cache.decorator import cache
from datetime import timedelta
from app.core.config import get_settings

settings = get_settings()
router = APIRouter(tags=["schools"])

@router.get("/", response_model=List[dict])
@cache(expire=timedelta(seconds=settings.CACHE_EXPIRATION_SECONDS))
async def get_schools(db: AsyncSession = Depends(get_db)):
    """Get all schools"""
    query = select(SchoolDB)
    result = await db.execute(query)
    schools = result.scalars().all()
    return [
        {
            "id": school.id,
            "name": school.name,
            "address": school.address,
            "logo": school.logo,
            "foundation_date": school.foundation_date.isoformat()
        }
        for school in schools
    ] 