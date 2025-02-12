from .courses_router import router as courses_router
from .schools import router as schools_router
from .platforms import router as platforms_router

__all__ = ['courses_router', 'schools_router', 'platforms_router'] 