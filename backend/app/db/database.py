from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from app.core.config import get_settings
from contextlib import asynccontextmanager
import logging
import time
import threading
import asyncio

logger = logging.getLogger(__name__)
settings = get_settings()

# Async engine
async_engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DB_ECHO,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_timeout=settings.DB_POOL_TIMEOUT
)

# Sync engine for scripts
sync_engine = create_engine(
    settings.DATABASE_URL.replace("postgresql+asyncpg", "postgresql"),
    echo=settings.DB_ECHO,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_timeout=settings.DB_POOL_TIMEOUT
)

# Async session
async_session_maker = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# Sync session for scripts
SessionLocal = sessionmaker(
    bind=sync_engine,
    autocommit=False,
    autoflush=False
)

class DatabaseManager:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._engine = None
                    cls._instance._session_factory = None
        return cls._instance

    async def initialize(self):
        """Initialize the database engine and session factory"""
        if self._engine is None:
            self._engine = async_engine
            self._session_factory = async_session_maker
        return self._engine

    @property
    def session_factory(self):
        if self._session_factory is None:
            asyncio.run(self.initialize())
        return self._session_factory

db_manager = DatabaseManager()

async def get_db():
    """Async dependency function to get DB session"""
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except SQLAlchemyError as e:
            logger.error(f"Database session error: {str(e)}")
            await session.rollback()
            raise
        finally:
            await session.close()

@asynccontextmanager
async def get_db_context():
    """Async context manager for database sessions"""
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except SQLAlchemyError as e:
            logger.error(f"Database error: {str(e)}")
            await session.rollback()
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            await session.rollback()
            raise
        finally:
            await session.close()

async def get_async_session() -> AsyncSession:
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close() 