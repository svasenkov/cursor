import logging
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from .database import async_session_maker

logger = logging.getLogger(__name__)

async def check_db_connection() -> bool:
    """Check database connection"""
    try:
        async with async_session_maker() as session:
            # Test the connection with a simple query
            result = await session.execute(text("SELECT 1"))
            value = result.scalar()  # Remove await here since scalar() is not a coroutine
            logger.info(f"Database connection check result: {value}")
            return True
    except Exception as e:
        logger.error(f"Database connection check failed: {str(e)}")
        # Log additional connection details
        from app.core.config import get_settings
        settings = get_settings()
        logger.error(f"Database host: {settings.POSTGRES_HOST}")
        logger.error(f"Database port: {settings.POSTGRES_PORT}")
        logger.error(f"Database name: {settings.POSTGRES_DB}")
        return False 