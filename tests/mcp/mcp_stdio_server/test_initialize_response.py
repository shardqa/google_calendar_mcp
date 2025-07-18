import json
import pytest
from unittest.mock import patch
from src.mcp.servers.mcp_stdio_server import MCPStdioServer
from .mocks import MockStdin, run_server_with_timeout, create_initialize_request, find_response_by_id


class TestInitializeResponse:
    
    def test_server_responds_to_initialize_request(self):
        server = MCPStdioServer()
        initialize_request = create_initialize_request()
        mock_stdin = MockStdin([json.dumps(initialize_request)])
        responses = []
        
        def capture_print(*args, **kwargs):
            if args:
                responses.append(args[0])
        
        with patch('sys.stdin', mock_stdin), \
             patch('builtins.print', side_effect=capture_print):
            
            run_server_with_timeout(server)
        
        assert len(responses) >= 1
        
        initialize_response = find_response_by_id(responses, 1)
        assert initialize_response is not None, "Should respond to initialize request"
        assert initialize_response["jsonrpc"] == "2.0"
        assert initialize_response["id"] == 1
        assert "result" in initialize_response
        assert "serverInfo" in initialize_response["result"] 