from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Course API"
    API_V1_STR: str = "/api/v1"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "development"
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # Database settings
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_HOST: Optional[str] = None
    POSTGRES_PORT: Optional[str] = None
    POSTGRES_DB: Optional[str] = None
    DATABASE_URL: Optional[str] = None
    
    # Server settings
    HOST: Optional[str] = None
    PORT: Optional[int] = None
    DEBUG: Optional[bool] = None
    
    # Other settings
    LOG_LEVEL: Optional[str] = None
    LOG_FORMAT: Optional[str] = None
    LOG_FILE: Optional[str] = None
    CACHE_EXPIRATION_SECONDS: Optional[int] = None
    DB_ECHO: Optional[bool] = None
    DB_POOL_SIZE: Optional[int] = None
    DB_MAX_OVERFLOW: Optional[int] = None
    DB_POOL_TIMEOUT: Optional[int] = None
    RATE_LIMIT_REQUESTS_PER_MINUTE: Optional[int] = None
    RATE_LIMIT_CLEANUP_INTERVAL: Optional[int] = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow"  # Allow extra fields
    )

_settings = Settings()

def get_settings() -> Settings:
    return _settings 