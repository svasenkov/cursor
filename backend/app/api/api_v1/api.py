from fastapi import APIRouter
from app.routers.courses_router import router as courses_router

api_router = APIRouter()
api_router.include_router(
    courses_router,
    prefix="/courses", 
    tags=["courses"]
) 