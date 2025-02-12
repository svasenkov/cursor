from fastapi import Request, Response
from fastapi.responses import JSONResponse
import time
import logging
from .rate_limiter import RateLimiter
from app.core.config import get_settings
from typing import Callable
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)
settings = get_settings()
rate_limiter = RateLimiter(
    requests_per_minute=settings.RATE_LIMIT_REQUESTS_PER_MINUTE,
    cleanup_interval=settings.RATE_LIMIT_CLEANUP_INTERVAL
)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        start_time = time.time()
        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            logger.info(
                f"Path: {request.url.path} "
                f"Method: {request.method} "
                f"Status: {response.status_code} "
                f"Duration: {process_time:.3f}s"
            )
            return response
        except Exception as e:
            process_time = time.time() - start_time
            logger.error(
                f"Error processing request: {str(e)} "
                f"Path: {request.url.path} "
                f"Method: {request.method} "
                f"Duration: {process_time:.3f}s"
            )
            raise

async def logging_middleware(request: Request, call_next: Callable) -> Response:
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    logger.info(
        f"Path: {request.url.path} "
        f"Method: {request.method} "
        f"Status: {response.status_code} "
        f"Duration: {process_time:.3f}s"
    )
    
    return response

async def rate_limit_middleware(request: Request, call_next: Callable) -> Response:
    # Simple rate limiting - can be enhanced with Redis or other storage
    return await call_next(request) 