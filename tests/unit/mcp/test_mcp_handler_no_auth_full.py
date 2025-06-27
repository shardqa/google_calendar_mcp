import io, json, types

import pytest

import src.mcp.mcp_handler_no_auth as mod

class DummySocket(io.BytesIO):
    def makefile(self, *args, **kwargs):
        return self
    def sendall(self, data):
        # Accept data written by BaseHTTPRequestHandler
        self.write(data)


def create_handler(path: str, method: str = "GET", body: bytes = b""):
    request_line = f"{method} {path} HTTP/1.1\r\n".encode()
    headers = b"Host: localhost\r\nContent-Length: %d\r\n\r\n" % len(body)
    raw_request = request_line + headers + body

    sock = DummySocket(raw_request)
    handler = mod.CalendarMCPHandlerNoAuth(sock, ("127.0.0.1", 0), None)
    handler._dummy_socket = sock
    # Override wfile to capture output
    handler.wfile = io.BytesIO()
    handler.rfile = io.BytesIO(body)
    return handler


def test_handle_root():
    h = create_handler("/", "GET")
    h.handle_root()
    h.wfile.seek(0)
    raw = h.wfile.read().decode()
    json_part = raw.split('\r\n\r\n',1)[-1]
    data = json.loads(json_part)
    assert data["status"] == "running"


def test_handle_sse_connection(monkeypatch):
    # Monkeypatch schema to minimal result to avoid heavy deps
    monkeypatch.setattr(mod, "get_mcp_schema", lambda: {"tools": []})
    h = create_handler("/sse", "GET")
    h.handle_sse_connection()
    h.wfile.seek(0)
    out = h.wfile.read().decode()
    assert "event: message" in out and "mcp/hello" in out


def test_handle_sse_post(monkeypatch):
    # Prepare fake handle_post_sse that echoes back
    def fake_post(handler, request, response):
        response["result"] = {"ok": True}
        handler.send_response(200)
        handler.send_header("Content-Type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(response).encode())

    monkeypatch.setattr(mod, "handle_post_sse", fake_post)

    body = json.dumps({"jsonrpc": "2.0", "id": 1}).encode()
    h = create_handler("/sse", "POST", body)
    h.headers["Content-Length"] = str(len(body))
    h.handle_sse_post()
    h.wfile.seek(0)
    raw = h.wfile.read().decode()
    json_part = raw.split('\r\n\r\n',1)[-1]
    data = json.loads(json_part)
    assert data["result"]["ok"] is True 


def test_do_options():
    h = create_handler("/", "OPTIONS")
    h.do_OPTIONS()
    # Ensure headers captured even if wfile was closed
    try:
        data_bytes = h.wfile.getvalue()
    except ValueError:
        data_bytes = h._dummy_socket.getvalue()
    assert b"Access-Control-Allow-Methods" in data_bytes 


def test_not_found_errors():
    # Test GET to unknown path
    h_get = create_handler("/unknown", "GET")
    h_get.do_GET()
    assert b"404" in h_get.wfile.getvalue()

    # Test POST to unknown path
    h_post = create_handler("/unknown", "POST", b"{}")
    h_post.do_POST()
    assert b"404" in h_post.wfile.getvalue()


def test_sse_post_internal_error(monkeypatch):
    def fake_post_raises(handler, req, resp):
        raise ValueError("test error")
    monkeypatch.setattr(mod, "handle_post_sse", fake_post_raises)

    body = json.dumps({"jsonrpc": "2.0"}).encode()
    h = create_handler("/sse", "POST", body)
    h.headers["Content-Length"] = str(len(body))
    h.handle_sse_post()

    raw = h.wfile.getvalue().decode()
    json_part = raw.split("\r\n\r\n", 1)[-1]
    data = json.loads(json_part)
    assert data["error"]["code"] == -32603
    assert "test error" in data["error"]["message"] 