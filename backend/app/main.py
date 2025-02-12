from datetime import datetime
from typing import Dict, Any, Optional
import logging
from fastapi import FastAPI, Request, Depends, HTTPException, status
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
from app.db.repositories.course_repository import CourseRepository
from app.services.course_service import CourseService
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.schemas.course import CourseListResponse
from app.api.api_v1.api import api_router
from pydantic import BaseModel

# Setup logging
setup_logging()
settings = get_settings()
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Add middleware
app.add_middleware(LoggingMiddleware)

# Add CORS middleware with proper origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Include routers with API prefix
app.include_router(api_router, prefix=settings.API_V1_STR)

# Include additional routers
app.include_router(courses_router, prefix="/api/courses", tags=["courses"])
app.include_router(schools_router, prefix="/api/schools", tags=["schools"])
app.include_router(platforms_router, prefix="/api/platforms", tags=["platforms"])

class Course(BaseModel):
    title: str
    description: str
    instructor: str
    duration: int

# In-memory storage for testing
courses = {}
last_id = 0

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/api/courses")
def get_courses():
    return list(courses.values())

@app.get("/api/courses/{course_id}")
def get_course(course_id: int):
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    return courses[course_id]

@app.post("/api/courses", status_code=status.HTTP_201_CREATED)
def create_course(course: Course):
    global last_id
    last_id += 1
    course_dict = course.model_dump()
    course_dict["id"] = last_id
    courses[last_id] = course_dict
    return course_dict

@app.put("/api/courses/{course_id}")
def update_course(course_id: int, course: Course):
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    course_dict = course.model_dump()
    course_dict["id"] = course_id
    courses[course_id] = course_dict
    return course_dict

@app.delete("/api/courses/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: int):
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    del courses[course_id]

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

@app.get("/api/courses", response_model=CourseListResponse)
async def get_courses(
    skip: int = 0,
    limit: int = 10,
    engineer_level: Optional[str] = None,
    search_term: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    course_service = CourseService(db)
    return await course_service.get_courses(
        skip=skip,
        limit=limit,
        engineer_level=engineer_level,
        search_term=search_term
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 