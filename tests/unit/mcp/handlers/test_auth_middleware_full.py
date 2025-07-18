import io, types, json, sys, time, importlib, os
from types import SimpleNamespace
import base64
import hmac
import hashlib

import pytest
from unittest.mock import MagicMock

import src.mcp.auth_middleware as am

class DummyHandler:
    def __init__(self, token: str, client_ip: str = "127.0.0.1", cert=None):
        self.headers = {"X-Forwarded-For": client_ip}
        if token:
            self.headers["Authorization"] = f"Bearer {token}"
        self.client_address = (client_ip, 12345)
        self.status_sent = None
        self.headers_sent = {}
        self.wfile = io.BytesIO()
        self.cert = cert

    # Stubs used by middleware
    def send_response(self, code):
        self.status_sent = code
    def send_header(self, k, v):
        self.headers_sent[k] = v
    def end_headers(self):
        pass

def test_authenticate_request_success(monkeypatch):
    auth = am.RobustAuthMiddleware()
    auth.allowed_ips = set()

    token = auth.generate_secure_token(client_ip="8.8.8.8")
    handler = DummyHandler(token, client_ip="8.8.8.8")

    ok, err = auth.authenticate_request(handler)
    assert ok and err is None
    # Should have auth_payload set
    assert hasattr(handler, "auth_payload")


def test_require_auth_wrapper(monkeypatch):
    auth = am.RobustAuthMiddleware()
    auth.allowed_ips = set()
    token = auth.generate_secure_token(client_ip="7.7.7.7")

    @auth.require_auth
    def hello(h):
        h.wfile.write(b"hi")

    handler = DummyHandler(token, client_ip="7.7.7.7")
    hello(handler)
    handler.wfile.seek(0)
    assert handler.wfile.read() == b"hi"


def test_authenticate_request_failure(monkeypatch):
    auth = am.RobustAuthMiddleware()
    auth.allowed_ips = {"10.0.0.1"}

    bad_token = "invalid.token"
    handler = DummyHandler(bad_token, client_ip="11.11.11.11")

    ok, err = auth.authenticate_request(handler)
    assert not ok and "Invalid token format" in err
    # Failed attempt should be logged
    assert auth.rate_limiter.failed_attempts["11.11.11.11"]


def test_get_client_ip_variations():
    auth = am.RobustAuthMiddleware()
    handler = DummyHandler("tok", client_ip="1.1.1.1")

    # Remove existing forwarded header to test Real-IP path
    handler.headers.pop("X-Forwarded-For", None)
    handler.headers["X-Real-IP"] = "2.2.2.2"
    assert auth._get_client_ip(handler) == "2.2.2.2"

    handler.headers["X-Forwarded-For"] = "3.3.3.3"
    assert auth._get_client_ip(handler) == "3.3.3.3"


def test_require_auth_failure(monkeypatch):
    auth = am.RobustAuthMiddleware()
    # Ensure any IP allowed to reach IP whitelist step
    auth.allowed_ips = set()

    @auth.require_auth
    def protected(h):
        h.wfile.write(b'ok')

    bad_handler = DummyHandler("bad.token", client_ip="4.4.4.4")
    protected(bad_handler)
    bad_handler.wfile.seek(0)
    output = bad_handler.wfile.read().decode()
    assert 'Authentication failed' in output

def test_fixed_token_flow(monkeypatch):
    monkeypatch.setenv("MCP_FIXED_TOKEN", "my-secret-test-token")
    auth = am.RobustAuthMiddleware()
    assert auth.fixed_token == "my-secret-test-token"

    # Test successful verification
    is_valid, payload, err = auth.verify_fixed_token("my-secret-test-token")
    assert is_valid and payload['token_type'] == 'fixed' and err is None

    # Test failed verification
    is_valid, _, err = auth.verify_fixed_token("wrong-token")
    assert not is_valid and "Invalid fixed token" in err

    # Test via main bearer token method
    is_valid, _, _ = auth.verify_bearer_token("my-secret-test-token")
    assert is_valid

    # Test via full request handler
    handler = DummyHandler("my-secret-test-token")
    is_valid, _ = auth.authenticate_request(handler)
    assert is_valid

def test_ip_whitelist_checker(monkeypatch):
    monkeypatch.setenv("MCP_ALLOWED_IPS", "10.0.0.0/24, 192.168.1.1")
    auth = am.RobustAuthMiddleware()

    assert auth.check_ip_whitelist("10.0.0.15")
    assert auth.check_ip_whitelist("192.168.1.1")
    assert not auth.check_ip_whitelist("192.168.1.2")
    assert not auth.check_ip_whitelist("1.1.1.1")
    # Bad IP should fail gracefully
    assert not auth.check_ip_whitelist("not-an-ip")

def test_authenticate_request_no_token(monkeypatch):
    handler = DummyHandler(token=None)
    auth = am.RobustAuthMiddleware()
    is_valid, _ = auth.authenticate_request(handler)
    assert not is_valid 