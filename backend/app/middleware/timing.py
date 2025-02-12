from fastapi import Request
import time
import logging
from app.core.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

async def timing_middleware(request: Request, call_next):
    """Middleware to log request timing"""
    if not settings.DEBUG:
        return await call_next(request)
        
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    
    logger.debug(
        f"Request: {request.method} {request.url.path} "
        f"Time: {process_time:.2f}ms "
        f"Status: {response.status_code}"
    )
    
    response.headers["X-Process-Time"] = f"{process_time:.2f}ms"
    return response 