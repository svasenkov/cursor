from datetime import datetime
from typing import Dict, Any
import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from app.models.errors import ErrorResponse, ValidationError
from app.core.config import get_settings
from app.core.logging_config import setup_logging
from app.middleware.middleware import LoggingMiddleware
from app.routers.courses_router import router as courses_router
from app.routers.schools import router as schools_router
from app.routers.platforms import router as platforms_router
from app.db.utils import check_db_connection

# Setup logging
setup_logging()
settings = get_settings()
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Add middleware
app.add_middleware(LoggingMiddleware)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)

# Include routers with API prefix
app.include_router(courses_router, prefix="/api/courses", tags=["courses"])
app.include_router(schools_router, prefix="/api/schools", tags=["schools"])
app.include_router(platforms_router, prefix="/api/platforms", tags=["platforms"])

@app.get("/api/health")
async def health_check() -> Dict[str, Any]:
    """Health check endpoint"""
    try:
        # Check database connection
        db_healthy = await check_db_connection()
        
        # Determine overall status
        status = "healthy" if db_healthy else "unhealthy"
        status_code = 200 if db_healthy else 503

        # Create response data
        health_status = {
            "status": status,
            "timestamp": datetime.now().isoformat(),
            "components": {
                "database": "healthy" if db_healthy else "unhealthy",
                "api": "healthy"
            },
            "version": settings.APP_VERSION,
            "environment": settings.APP_ENV
        }

        if not db_healthy:
            logger.warning("Health check failed - database connection issue")
        else:
            logger.info("Health check passed")

        return JSONResponse(
            status_code=status_code,
            content=health_status
        )

    except Exception as e:
        logger.error(f"Health check failed with error: {str(e)}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "timestamp": datetime.now().isoformat(),
                "components": {
                    "database": "unhealthy",
                    "api": "unhealthy"
                },
                "error": str(e)
            }
        )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors"""
    errors = [
        ValidationError(
            field=error["loc"][-1],
            message=error["msg"]
        )
        for error in exc.errors()
    ]
    return JSONResponse(
        status_code=422,
        content=ErrorResponse(
            detail="Validation error",
            error_code="VALIDATION_ERROR",
            metadata={"errors": [error.dict() for error in errors]}
        ).dict()
    )

@app.on_event("startup")
async def startup_event():
    """Initialize cache on startup"""
    FastAPICache.init(InMemoryBackend())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 