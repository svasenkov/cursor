from typing import Dict, List, Optional
from collections import defaultdict
import time
import threading

class RateLimiter:
    def __init__(self, requests_per_minute: int = 100, cleanup_interval: int = 300):
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, List[float]] = defaultdict(list)
        self.cleanup_interval = cleanup_interval
        self.last_cleanup = time.time()
        self._lock = threading.Lock()  # Add thread safety

    async def cleanup(self) -> None:
        """Periodically clean up old requests to prevent memory leaks"""
        now = time.time()
        if now - self.last_cleanup > self.cleanup_interval:
            with self._lock:
                minute_ago = now - 60
                # More efficient cleanup using dict comprehension
                self.requests = defaultdict(list, {
                    ip: [t for t in times if t > minute_ago]
                    for ip, times in self.requests.items()
                    if times  # Only keep IPs with remaining requests
                })
                self.last_cleanup = now

    async def is_rate_limited(self, client_ip: str) -> bool:
        """
        Check if a client IP is rate limited
        Returns True if rate limited, False otherwise
        """
        await self.cleanup()
        now = time.time()
        minute_ago = now - 60
        
        with self._lock:
            # Filter old requests in one pass
            recent_requests = [t for t in self.requests[client_ip] if t > minute_ago]
            
            if len(recent_requests) >= self.requests_per_minute:
                return True
                
            recent_requests.append(now)
            self.requests[client_ip] = recent_requests
            return False

    def get_remaining_requests(self, client_ip: str) -> Optional[int]:
        """Get remaining requests for an IP address"""
        now = time.time()
        minute_ago = now - 60
        
        with self._lock:
            recent_requests = len([t for t in self.requests[client_ip] if t > minute_ago])
            return max(0, self.requests_per_minute - recent_requests) 