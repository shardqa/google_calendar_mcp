import pytest
import src.scripts.test_sse_stream as sse_module
from _pytest.outcomes import Failed

class DummyResponse:
    def __init__(self, status_code, lines):
        self.status_code = status_code
        self._lines = lines
        self.closed = False
        self.text = None
    def iter_lines(self, chunk_size=512):
        return self._lines
    def close(self):
        self.closed = True

class DummySession:
    def __init__(self, response):
        self._response = response
    def get(self, url, headers, stream, timeout):
        return self._response

class DummySessionFactory:
    def __init__(self, response):
        self._response = response
    def __call__(self):
        return DummySession(self._response)

def test_status_not_200(monkeypatch, capsys):
    monkeypatch.setattr(sse_module.cancel_utils, 'get_sse_url', lambda url: 'http://example.com')
    response = DummyResponse(status_code=404, lines=[])
    response.text = "Not Found"
    monkeypatch.setattr(sse_module.requests, 'Session', DummySessionFactory(response))
    with pytest.raises(Failed) as excinfo:
        sse_module.test_sse_stream_read("http://dummy-url.com/sse")
    assert 'Error: Unexpected status code 404' in excinfo.value.msg

def test_open_exception(monkeypatch, capsys):
    monkeypatch.setattr(sse_module.cancel_utils, 'get_sse_url', lambda url: 'http://example.com')
    class BadSession:
        def get(self, url, headers, stream, timeout):
            raise Exception('open fail')
    monkeypatch.setattr(sse_module.requests, 'Session', lambda: BadSession())
    with pytest.raises(Failed) as excinfo:
        sse_module.test_sse_stream_read("http://dummy-url.com/sse")
    assert 'An error occurred during stream setup or initial reading: open fail' in excinfo.value.msg

def test_successful_stream(monkeypatch, capsys):
    monkeypatch.setattr(sse_module.cancel_utils, 'get_sse_url', lambda url: 'http://example.com')
    lines = [b'event: test_event', b'data: {"key":"value"}', b':', b'event: mcp/hello', b'data: {}', b'event: tools/list', b'data: []']
    response = DummyResponse(status_code=200, lines=lines)
    monkeypatch.setattr(sse_module.requests, 'Session', DummySessionFactory(response))
    sse_module.test_sse_stream_read("http://dummy-url.com/sse") 