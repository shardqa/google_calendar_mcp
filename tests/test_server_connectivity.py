import pytest
import src.test_server as server

class DummySock:
    def __init__(self, result):
        self._result = result
    def settimeout(self, t):
        pass
    def connect_ex(self, addr):
        return self._result
    def close(self):
        pass

class DummyResp:
    def __init__(self, status_code, text=''):
        self.status_code = status_code
        self.text = text

def test_socket_fail(monkeypatch):
    sock = DummySock(result=1)
    monkeypatch.setattr(server.socket, 'socket', lambda *args, **kwargs: sock)
    assert server.check_server_connectivity('localhost', 1234) is False

def test_http_get_fail(monkeypatch):
    sock = DummySock(result=0)
    monkeypatch.setattr(server.socket, 'socket', lambda *args, **kwargs: sock)
    monkeypatch.setattr(server.requests, 'get', lambda *args, **kwargs: (_ for _ in ()).throw(Exception('fail')))
    assert server.check_server_connectivity('localhost', 3001) is False

def test_post_fail(monkeypatch):
    sock = DummySock(result=0)
    monkeypatch.setattr(server.socket, 'socket', lambda *args, **kwargs: sock)
    monkeypatch.setattr(server.requests, 'get', lambda *args, **kwargs: DummyResp(200, 'ok'))
    monkeypatch.setattr(server.requests, 'post', lambda *args, **kwargs: (_ for _ in ()).throw(Exception('fail')))
    assert server.check_server_connectivity('localhost', 3001) is False

def test_all_success(monkeypatch):
    sock = DummySock(result=0)
    monkeypatch.setattr(server.socket, 'socket', lambda *args, **kwargs: sock)
    monkeypatch.setattr(server.requests, 'get', lambda *args, **kwargs: DummyResp(200, 'hello'))
    monkeypatch.setattr(server.requests, 'post', lambda *args, **kwargs: DummyResp(200, 'world'))
    assert server.check_server_connectivity('localhost', 3001) is True 