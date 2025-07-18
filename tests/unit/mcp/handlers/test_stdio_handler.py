import pytest
from unittest.mock import MagicMock
from src.mcp.handlers.stdio_handler import StdioRequestHandler

@pytest.fixture
def capabilities():
    return {
        "tools": {"echo": {}},
        "serverInfo": {"name": "test-server"},
        "protocolVersion": "test-protocol"
    }

def test_handle_initialize(capabilities):
    handler = StdioRequestHandler(capabilities)
    request = {"jsonrpc": "2.0", "id": 1, "method": "initialize"}
    response = handler.handle_request(request)
    assert response['id'] == 1
    assert response['result']['serverInfo']['name'] == "test-server"

def test_handle_tools_list(capabilities, monkeypatch):
    monkeypatch.setattr('src.mcp.stdio_handler.get_mcp_schema', lambda: {"tools": [{"name": "echo"}]})
    handler = StdioRequestHandler(capabilities)
    request = {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}
    response = handler.handle_request(request)
    assert response['id'] == 2
    assert response['result']['tools'][0]['name'] == "echo"

def test_handle_unknown_method(capabilities):
    handler = StdioRequestHandler(capabilities)
    request = {"jsonrpc": "2.0", "id": 3, "method": "unknown"}
    response = handler.handle_request(request)
    assert response['id'] == 3
    assert response['error']['code'] == -32601

def test_handle_tools_call(capabilities, monkeypatch):
    mock_post_handler = MagicMock()
    monkeypatch.setattr('src.mcp.stdio_handler.handle_post_other', mock_post_handler)
    
    handler = StdioRequestHandler(capabilities)
    request = {"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {}}
    handler.handle_request(request)
    
    mock_post_handler.assert_called_once() 