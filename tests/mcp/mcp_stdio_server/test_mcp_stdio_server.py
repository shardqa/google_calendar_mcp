import pytest
import json
import threading
import time
from unittest.mock import patch, MagicMock
from io import StringIO
import sys
from src.mcp.mcp_stdio_server import MCPStdioServer


class MockStdin:
    def __init__(self, input_data):
        self.input_data = input_data
        self.position = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.position < len(self.input_data):
            line = self.input_data[self.position]
            self.position += 1
            return line
        raise StopIteration


class TestMCPStdioServer:
    
    def test_server_should_not_send_hello_automatically(self):
        """Test that server does not send hello message automatically on start.
        According to MCP protocol, server should only respond to client requests."""
        
        server = MCPStdioServer()
        output_buffer = StringIO()
        
        # Mock stdin to provide empty input (no client requests)
        mock_stdin = MockStdin([])
        
        with patch('sys.stdout', output_buffer), \
             patch('sys.stdin', mock_stdin), \
             patch('builtins.print') as mock_print:
            
            # Start server in a thread with timeout to avoid hanging
            def run_server():
                try:
                    server.start()
                except Exception:
                    pass
            
            thread = threading.Thread(target=run_server)
            thread.daemon = True
            thread.start()
            thread.join(timeout=0.1)  # Short timeout
            
            # Server should NOT have sent any hello message automatically
            # mock_print should not have been called with hello message
            if mock_print.called:
                for call in mock_print.call_args_list:
                    printed_data = call[0][0] if call[0] else ""
                    if "mcp/hello" in printed_data:
                        pytest.fail("Server should not send hello message automatically")
    
    def test_server_responds_to_initialize_request(self):
        """Test that server properly responds to initialize request."""
        
        server = MCPStdioServer()
        
        # Prepare initialize request
        initialize_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {}
        }
        
        mock_stdin = MockStdin([json.dumps(initialize_request)])
        responses = []
        
        def capture_print(*args, **kwargs):
            if args:
                responses.append(args[0])
        
        with patch('sys.stdin', mock_stdin), \
             patch('builtins.print', side_effect=capture_print):
            
            def run_server():
                try:
                    server.start()
                except Exception:
                    pass
            
            thread = threading.Thread(target=run_server)
            thread.daemon = True
            thread.start()
            thread.join(timeout=0.2)
        
        # Should have received proper initialize response
        assert len(responses) >= 1
        
        # Find the initialize response (ignore any hello messages)
        initialize_response = None
        for response_str in responses:
            try:
                response = json.loads(response_str)
                if response.get("id") == 1 and "result" in response:
                    initialize_response = response
                    break
            except json.JSONDecodeError:
                continue
        
        assert initialize_response is not None, "Should respond to initialize request"
        assert initialize_response["jsonrpc"] == "2.0"
        assert initialize_response["id"] == 1
        assert "result" in initialize_response
        assert "serverInfo" in initialize_response["result"] 