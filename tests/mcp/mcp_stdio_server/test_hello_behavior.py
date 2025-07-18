import pytest
from unittest.mock import patch
from io import StringIO
from src.mcp.servers.mcp_stdio_server import MCPStdioServer
from .mocks import MockStdin, run_server_with_timeout


class TestHelloBehavior:
    
    def test_server_should_not_send_hello_automatically(self):
        server = MCPStdioServer()
        output_buffer = StringIO()
        mock_stdin = MockStdin([])
        
        with patch('sys.stdout', output_buffer), \
             patch('sys.stdin', mock_stdin), \
             patch('builtins.print') as mock_print:
            
            run_server_with_timeout(server, timeout=0.1)
            
            if mock_print.called:
                for call in mock_print.call_args_list:
                    printed_data = call[0][0] if call[0] else ""
                    if "mcp/hello" in printed_data:
                        pytest.fail("Server should not send hello message automatically") 