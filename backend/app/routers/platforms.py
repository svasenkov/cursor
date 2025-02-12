from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.db.models import PlatformDB
from app.models.platform import Platform
from fastapi_cache.decorator import cache
from datetime import timedelta
from app.core.config import get_settings
from sqlalchemy import select

settings = get_settings()
router = APIRouter(tags=["platforms"])

@router.get("/", response_model=List[dict])
async def get_platforms(db: AsyncSession = Depends(get_db)):
    """Get all platforms"""
    query = select(PlatformDB)
    result = await db.execute(query)
    platforms = result.scalars().all()
    return [
        {
            "id": platform.id,
            "name": platform.name,
            "url": platform.url,
            "logo": platform.logo,
            "description": platform.description,
            "features": platform.features
        }
        for platform in platforms
    ]

@router.get("/{platform_name}", response_model=Platform)
async def get_platform(platform_name: str, db: AsyncSession = Depends(get_db)):
    """Get platform by name"""
    query = select(PlatformDB).where(PlatformDB.name == platform_name)
    result = await db.execute(query)
    platform = result.scalars().first()
    if platform is None:
        raise HTTPException(status_code=404, detail="Platform not found")
    return platform 