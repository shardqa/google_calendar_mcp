import json
from typing import Dict, Any, Optional
from ..mcp_schema import get_mcp_schema
from .mcp_post_other_handler import handle_post_other

class MockHandler:
    """Mocks the behavior of a BaseHTTPRequestHandler for capturing responses."""
    def __init__(self):
        self.response_data = None
        self.status_code = 200
        self.headers = []
    
    def send_response(self, code):
        self.status_code = code
    
    def send_header(self, key, value):
        self.headers.append((key, value))
    
    def end_headers(self):
        pass
    
    @property
    def wfile(self):
        class MockWFile:
            def __init__(self, handler):
                self.handler = handler
            
            def write(self, data):
                if isinstance(data, bytes):
                    data = data.decode('utf-8')
                try:
                    self.handler.response_data = json.loads(data)
                except json.JSONDecodeError:
                    self.handler.response_data = {"error": "Invalid JSON response"}
        
        return MockWFile(self)

class StdioRequestHandler:
    def __init__(self, capabilities: Dict):
        self.capabilities = capabilities

    def handle_request(self, request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        method = request.get("method")
        
        if method == "initialize":
            return self._handle_initialize(request)
        elif method == "tools/list":
            return self._handle_tools_list(request)
        elif method == "tools/call":
            return self._handle_tools_call(request)
        else:
            return {
                "jsonrpc": request.get("jsonrpc", "2.0"),
                "id": request.get("id"),
                "error": {"code": -32601, "message": f"Method not found: {method}"}
            }

    def _handle_initialize(self, request: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "jsonrpc": request.get("jsonrpc", "2.0"),
            "id": request.get("id"),
            "result": {
                "serverInfo": self.capabilities["serverInfo"],
                "capabilities": {"tools": self.capabilities["tools"]},
                "protocolVersion": self.capabilities["protocolVersion"]
            }
        }

    def _handle_tools_list(self, request: Dict[str, Any]) -> Dict[str, Any]:
        schema = get_mcp_schema()
        return {
            "jsonrpc": request.get("jsonrpc", "2.0"),
            "id": request.get("id"),
            "result": {"tools": schema['tools']}
        }

    def _handle_tools_call(self, request: Dict[str, Any]) -> Dict[str, Any]:
        mock_handler = MockHandler()
        response = {"jsonrpc": request.get("jsonrpc", "2.0"), "id": request.get("id")}
        
        try:
            handle_post_other(mock_handler, request, response)
            if mock_handler.response_data:
                return mock_handler.response_data
            return response
        except Exception as e:
            return {
                "jsonrpc": request.get("jsonrpc", "2.0"),
                "id": request.get("id"),
                "error": {"code": -32603, "message": f"Internal error: {str(e)}"}
            } 