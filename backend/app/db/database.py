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
import sys
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import declarative_base

logger = logging.getLogger(__name__)
settings = get_settings()

# Use sqlite+aiosqlite:/// for async SQLite
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL.replace(
    "sqlite:///", "sqlite+aiosqlite:///", 1
)

# Create async engine
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=settings.DB_ECHO,
    future=True,
)

# Create async session maker
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()

# Create engines based on context
def create_engines():
    """Create appropriate database engines"""
    settings = get_settings()
    db_url = SQLALCHEMY_DATABASE_URL
    
    engine_args = {
        "echo": settings.DB_ECHO,
        "pool_size": settings.DB_POOL_SIZE,
        "max_overflow": settings.DB_MAX_OVERFLOW,
        "pool_timeout": settings.DB_POOL_TIMEOUT
    }
    
    if 'postgresql+asyncpg' in db_url:
        return create_async_engine(db_url, **engine_args)
    return create_engine(db_url, **engine_args)

engine = create_engines()

# Session factories
async_session_maker = sessionmaker(
    engine, 
    class_=AsyncSession,
    expire_on_commit=False
)

# Sync session for scripts/migrations
SessionLocal = sessionmaker(
    bind=engine,
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
            self._engine = engine
            self._session_factory = async_session_maker
        return self._engine

    @property
    def session_factory(self):
        if self._session_factory is None:
            asyncio.run(self.initialize())
        return self._session_factory

db_manager = DatabaseManager()

async def get_db() -> AsyncSession:
    """Dependency for getting async DB sessions"""
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()

@asynccontextmanager
async def get_db_context():
    """Context manager for DB sessions"""
    async with async_session_maker() as session:
        try:
            yield session
        except SQLAlchemyError as e:
            logger.error(f"Database error: {str(e)}")
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