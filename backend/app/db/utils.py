from sqlalchemy import text
from app.db.database import async_session_maker
import logging

logger = logging.getLogger(__name__)

async def check_db_connection() -> bool:
    """Check database connection by executing a simple query"""
    try:
        async with async_session_maker() as session:
            # Use text() to properly declare SQL expression
            await session.execute(text("SELECT 1"))
            await session.commit()
            return True
    except Exception as e:
        logger.error(f"Database connection check failed: {str(e)}")
        return False 