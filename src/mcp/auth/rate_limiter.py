import time
from typing import Dict, List

class RateLimiter:
    def __init__(self, max_requests: int = 100, window: int = 3600, max_failed: int = 10):
        self.max_requests = max_requests
        self.window = window
        self.max_failed = max_failed
        self.requests: Dict[str, List[float]] = {}
        self.failed_attempts: Dict[str, List[float]] = {}

    def check_rate_limit(self, client_ip: str) -> bool:
        now = time.time()
        
        if client_ip not in self.requests:
            self.requests[client_ip] = []
        
        timestamps = self.requests[client_ip]
        # Remove timestamps outside the window
        self.requests[client_ip] = [ts for ts in timestamps if now - ts < self.window]
        
        if len(self.requests[client_ip]) >= self.max_requests:
            return False
            
        self.requests[client_ip].append(now)
        return True

    def record_failed_attempt(self, client_ip: str) -> None:
        now = time.time()
        if client_ip not in self.failed_attempts:
            self.failed_attempts[client_ip] = []
        
        self.failed_attempts[client_ip].append(now)

    def is_ip_blocked(self, client_ip: str) -> bool:
        if client_ip not in self.failed_attempts:
            return False
        
        now = time.time()
        recent_attempts = [
            attempt for attempt in self.failed_attempts[client_ip] 
            if now - attempt < self.window
        ]
        self.failed_attempts[client_ip] = recent_attempts
        
        return len(recent_attempts) >= self.max_failed 