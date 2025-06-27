import pytest
import time
from src.mcp.auth.rate_limiter import RateLimiter

def test_rate_limiter():
    limiter = RateLimiter(max_requests=5, window=10)

    # 5 requests should be fine
    for _ in range(5):
        assert limiter.check_rate_limit("1.1.1.1") is True
    
    # 6th should be blocked
    assert limiter.check_rate_limit("1.1.1.1") is False

    # Different IP should be fine
    assert limiter.check_rate_limit("2.2.2.2") is True

def test_rate_limiter_window():
    limiter = RateLimiter(max_requests=2, window=0.1)
    assert limiter.check_rate_limit("1.1.1.1") is True
    assert limiter.check_rate_limit("1.1.1.1") is True
    assert limiter.check_rate_limit("1.1.1.1") is False
    time.sleep(0.1)
    # After window expires, new requests are allowed
    assert limiter.check_rate_limit("1.1.1.1") is True

def test_ip_blocking():
    limiter = RateLimiter(max_failed=3, window=10)

    limiter.record_failed_attempt("1.1.1.1")
    limiter.record_failed_attempt("1.1.1.1")
    assert limiter.is_ip_blocked("1.1.1.1") is False

    limiter.record_failed_attempt("1.1.1.1")
    assert limiter.is_ip_blocked("1.1.1.1") is True

    # Different IP is not blocked
    assert limiter.is_ip_blocked("2.2.2.2") is False

def test_ip_blocking_window():
    limiter = RateLimiter(max_failed=2, window=0.1)
    limiter.record_failed_attempt("1.1.1.1")
    limiter.record_failed_attempt("1.1.1.1")
    assert limiter.is_ip_blocked("1.1.1.1") is True
    time.sleep(0.1)
    # After window expires, IP is no longer blocked
    assert limiter.is_ip_blocked("1.1.1.1") is False 