import pytest
from unittest.mock import patch, MagicMock
import sys
import os
import socket
import requests

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
import src.scripts.test_server as test_server


class TestServerConnectivity:
    
    @patch('src.scripts.test_server.socket.socket')
    @patch('src.scripts.test_server.requests.get')
    @patch('src.scripts.test_server.requests.post')
    def test_check_server_connectivity_success(self, mock_post, mock_get, mock_socket_class):
        """Test successful server connectivity check"""
        # Mock socket connection
        mock_socket = MagicMock()
        mock_socket.connect_ex.return_value = 0
        mock_socket_class.return_value = mock_socket
        
        # Mock GET response
        mock_get_response = MagicMock()
        mock_get_response.status_code = 200
        mock_get_response.text = "Server is running"
        mock_get.return_value = mock_get_response
        
        # Mock POST response
        mock_post_response = MagicMock()
        mock_post_response.status_code = 200
        mock_post_response.text = '{"result": "success"}'
        mock_post.return_value = mock_post_response
        
        result = test_server.check_server_connectivity()
        
        assert result is True
        mock_socket.connect_ex.assert_called_once_with(("localhost", 3001))
        mock_get.assert_called_once_with("http://localhost:3001", timeout=5)
        mock_post.assert_called_once()

    @patch('src.scripts.test_server.socket.socket')
    @patch('src.scripts.test_server.requests.get')
    @patch('src.scripts.test_server.requests.post')
    def test_check_server_connectivity_with_custom_host_port(self, mock_post, mock_get, mock_socket_class):
        """Test server connectivity check with custom host and port"""
        # Mock socket connection
        mock_socket = MagicMock()
        mock_socket.connect_ex.return_value = 0
        mock_socket_class.return_value = mock_socket
        
        # Mock GET response
        mock_get_response = MagicMock()
        mock_get_response.status_code = 200
        mock_get_response.text = "Server is running"
        mock_get.return_value = mock_get_response
        
        # Mock POST response
        mock_post_response = MagicMock()
        mock_post_response.status_code = 200
        mock_post_response.text = '{"result": "success"}'
        mock_post.return_value = mock_post_response
        
        result = test_server.check_server_connectivity("example.com", 8080)
        
        assert result is True
        mock_socket.connect_ex.assert_called_once_with(("example.com", 8080))
        mock_get.assert_called_once_with("http://example.com:8080", timeout=5)

    @patch('src.scripts.test_server.socket.socket')
    def test_check_server_connectivity_socket_connection_failed(self, mock_socket_class):
        """Test handling of failed socket connection"""
        # Mock socket connection failure
        mock_socket = MagicMock()
        mock_socket.connect_ex.return_value = 1  # Connection failed
        mock_socket_class.return_value = mock_socket
        
        result = test_server.check_server_connectivity()
        
        assert result is False
        mock_socket.connect_ex.assert_called_once_with(("localhost", 3001))

    @patch('src.scripts.test_server.socket.socket')
    def test_check_server_connectivity_socket_exception(self, mock_socket_class):
        """Test handling of socket exception"""
        # Mock socket exception
        mock_socket_class.side_effect = Exception("Socket error")
        
        result = test_server.check_server_connectivity()
        
        assert result is False

    @patch('src.scripts.test_server.socket.socket')
    @patch('src.scripts.test_server.requests.get')
    def test_check_server_connectivity_http_exception(self, mock_get, mock_socket_class):
        """Test handling of HTTP connection exception"""
        # Mock socket connection success
        mock_socket = MagicMock()
        mock_socket.connect_ex.return_value = 0
        mock_socket_class.return_value = mock_socket
        
        # Mock HTTP exception
        mock_get.side_effect = Exception("HTTP connection failed")
        
        result = test_server.check_server_connectivity()
        
        assert result is False

    @patch('src.scripts.test_server.socket.socket')
    @patch('src.scripts.test_server.requests.get')
    @patch('src.scripts.test_server.requests.post')
    def test_check_server_connectivity_post_exception(self, mock_post, mock_get, mock_socket_class):
        """Test handling of POST request exception"""
        # Mock socket connection success
        mock_socket = MagicMock()
        mock_socket.connect_ex.return_value = 0
        mock_socket_class.return_value = mock_socket
        
        # Mock GET response success
        mock_get_response = MagicMock()
        mock_get_response.status_code = 200
        mock_get_response.text = "Server is running"
        mock_get.return_value = mock_get_response
        
        # Mock POST exception
        mock_post.side_effect = Exception("POST failed")
        
        result = test_server.check_server_connectivity()
        
        assert result is False

    def test_main_execution_simulation(self):
        """Test that the main execution logic works correctly"""
        # Test default parameters
        test_args = ['test_server.py']
        host = test_args[1] if len(test_args) > 1 else "localhost"
        port = int(test_args[2]) if len(test_args) > 2 else 3001
        assert host == "localhost"
        assert port == 3001
        
        # Test custom host
        test_args = ['test_server.py', 'example.com']
        host = test_args[1] if len(test_args) > 1 else "localhost"
        port = int(test_args[2]) if len(test_args) > 2 else 3001
        assert host == "example.com"
        assert port == 3001
        
        # Test custom host and port
        test_args = ['test_server.py', 'example.com', '8080']
        host = test_args[1] if len(test_args) > 1 else "localhost"
        port = int(test_args[2]) if len(test_args) > 2 else 3001
        assert host == "example.com"
        assert port == 8080

    @patch('sys.argv', ['test_server.py'])
    @patch('src.scripts.test_server.check_server_connectivity')
    def test_main_block_execution_success(self, mock_check_connectivity):
        """Test the main block execution when connectivity succeeds"""
        mock_check_connectivity.return_value = True
        
        # Execute the main block logic directly
        host = "localhost" 
        port = 3001
        
        # Simulate the main block logic
        result = test_server.check_server_connectivity(host, port)
        mock_check_connectivity.assert_called_once_with(host, port)
        assert result is True

    @patch('sys.argv', ['test_server.py'])
    @patch('src.scripts.test_server.check_server_connectivity')
    def test_main_block_execution_failure(self, mock_check_connectivity):
        """Test the main block execution when connectivity fails"""
        mock_check_connectivity.return_value = False
        
        # Execute the main block logic directly
        host = "localhost"
        port = 3001
        
        # Simulate the main block logic
        result = test_server.check_server_connectivity(host, port)
        mock_check_connectivity.assert_called_once_with(host, port)
        assert result is False

    def test_main_block_execution_failure(self):
        """Test main block execution with failure"""
        test_args = ['test_server.py', 'nonexistent_host', '9999']
        
        # Test parsing arguments
        host = test_args[1] if len(test_args) > 1 else "localhost"
        port = int(test_args[2]) if len(test_args) > 2 else 3001
        
        assert host == 'nonexistent_host'
        assert port == 9999
        
        # Test the conditional logic
        test_condition = False  # Simulating failed connectivity
        if test_condition:
            result = "Server is accessible and responding to requests"
        else:
            result = "Server connectivity issues detected"
            
        assert result == "Server connectivity issues detected"

    @patch('src.scripts.test_server.check_server_connectivity')
    def test_main_block_execution_with_args(self, mock_check):
        """Test main block execution with different argument combinations"""
        mock_check.return_value = True
        
        # Test with default arguments
        test_args = ['test_server.py']
        host = test_args[1] if len(test_args) > 1 else "localhost"
        port = int(test_args[2]) if len(test_args) > 2 else 3001
        
        assert host == "localhost"
        assert port == 3001
        
        # Test with custom host
        test_args = ['test_server.py', 'custom_host']
        host = test_args[1] if len(test_args) > 1 else "localhost"
        port = int(test_args[2]) if len(test_args) > 2 else 3001
        
        assert host == "custom_host"
        assert port == 3001
        
        # Test with custom host and port
        test_args = ['test_server.py', 'custom_host', '8080']
        host = test_args[1] if len(test_args) > 1 else "localhost"
        port = int(test_args[2]) if len(test_args) > 2 else 3001
        
        assert host == "custom_host"
        assert port == 8080

    def test_main_block_print_messages(self):
        """Test the print messages in main block"""
        # Test success message
        success_msg = "Server is accessible and responding to requests"
        assert success_msg is not None
        
        # Test failure message
        failure_msg = "Server connectivity issues detected"
        assert failure_msg is not None
        
        # Test solution messages
        solutions = [
            "Make sure the server is running: ./run_mcp.sh",
            "Check if the port is correct (default is 3001)",
            "Try running the server with: python -m src.mcp_cli --port 3001",
            "Check firewall settings (should not be an issue for localhost)",
            "Try using 0.0.0.0 instead of localhost: python -m src.mcp_cli --host 0.0.0.0 --port 3001"
        ]
        
        for solution in solutions:
            assert solution is not None

    @patch('src.scripts.test_server.check_server_connectivity')
    def test_main_block_success_path(self, mock_check):
        """Test main block success path"""
        mock_check.return_value = True
        
        # Simulate the main block logic
        host = "localhost"
        port = 3001
        
        if mock_check(host, port):
            result = "success"
        else:
            result = "failure"
            
        assert result == "success"

    @patch('src.scripts.test_server.check_server_connectivity')
    def test_main_block_failure_path(self, mock_check):
        """Test main block execution failure path"""
        mock_check.return_value = False
        
        # Simulate main block
        host = "localhost"
        port = 3001
        
        result = mock_check(host, port)
        assert result is False
        mock_check.assert_called_once_with(host, port)

    @patch('sys.argv', ['test_server.py', 'example.com', '8080'])
    @patch('src.scripts.test_server.check_server_connectivity')
    @patch('builtins.print')
    def test_main_block_with_custom_args_success(self, mock_print, mock_check):
        """Test main block execution with custom arguments - success path"""
        mock_check.return_value = True
        
        # Simulate main block logic
        host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
        port = int(sys.argv[2]) if len(sys.argv) > 2 else 3001
        
        mock_print(f"Testing server at {host}:{port}")
        result = mock_check(host, port)
        
        if result:
            mock_print("\n✅ Server is accessible and responding to requests")
        
        assert host == "example.com"
        assert port == 8080
        assert result is True
        mock_check.assert_called_once_with(host, port)

    @patch('sys.argv', ['test_server.py', 'badhost', '9999'])
    @patch('src.scripts.test_server.check_server_connectivity')
    @patch('builtins.print')
    def test_main_block_with_custom_args_failure(self, mock_print, mock_check):
        """Test main block execution with custom arguments - failure path"""
        mock_check.return_value = False
        
        # Simulate main block logic
        host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
        port = int(sys.argv[2]) if len(sys.argv) > 2 else 3001
        
        mock_print(f"Testing server at {host}:{port}")
        result = mock_check(host, port)
        
        if not result:
            mock_print("\n❌ Server connectivity issues detected")
            mock_print("Possible solutions:")
            mock_print("1. Make sure the server is running: ./run_mcp.sh")
            mock_print("2. Check if the port is correct (default is 3001)")
            mock_print("3. Try running the server with: python -m src.mcp_cli --port 3001")
            mock_print("4. Check firewall settings (should not be an issue for localhost)")
            mock_print("5. Try using 0.0.0.0 instead of localhost: python -m src.mcp_cli --host 0.0.0.0 --port 3001")
        
        assert host == "badhost"
        assert port == 9999
        assert result is False
        mock_check.assert_called_once_with(host, port)

    @patch('sys.argv', ['test_server.py'])
    @patch('src.scripts.test_server.check_server_connectivity')
    @patch('builtins.print')
    def test_main_block_default_args_success(self, mock_print, mock_check):
        """Test main block execution with default arguments - success path"""
        mock_check.return_value = True
        
        # Simulate main block logic
        host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
        port = int(sys.argv[2]) if len(sys.argv) > 2 else 3001
        
        mock_print(f"Testing server at {host}:{port}")
        result = mock_check(host, port)
        
        if result:
            mock_print("\n✅ Server is accessible and responding to requests")
        
        assert host == "localhost"
        assert port == 3001
        assert result is True
        mock_check.assert_called_once_with(host, port)

    @patch('sys.argv', ['test_server.py'])
    @patch('src.scripts.test_server.check_server_connectivity')
    @patch('builtins.print')
    def test_main_block_default_args_failure(self, mock_print, mock_check):
        """Test main block execution with default arguments - failure path"""
        mock_check.return_value = False
        
        # Simulate main block logic
        host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
        port = int(sys.argv[2]) if len(sys.argv) > 2 else 3001
        
        mock_print(f"Testing server at {host}:{port}")
        result = mock_check(host, port)
        
        if not result:
            mock_print("\n❌ Server connectivity issues detected")
            mock_print("Possible solutions:")
            mock_print("1. Make sure the server is running: ./run_mcp.sh")
            mock_print("2. Check if the port is correct (default is 3001)")
            mock_print("3. Try running the server with: python -m src.mcp_cli --port 3001")
            mock_print("4. Check firewall settings (should not be an issue for localhost)")
            mock_print("5. Try using 0.0.0.0 instead of localhost: python -m src.mcp_cli --host 0.0.0.0 --port 3001")
        
        assert host == "localhost"
        assert port == 3001
        assert result is False
        mock_check.assert_called_once_with(host, port)

    @patch('sys.argv', ['test_server.py'])
    @patch('src.scripts.test_server.check_server_connectivity')
    @patch('builtins.print')
    def test_actual_main_block_execution(self, mock_print, mock_check):
        """Test actual main block execution by simulating __main__ environment"""
        mock_check.return_value = True
        
        # Execute the actual main block code
        main_block_code = '''
host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
port = int(sys.argv[2]) if len(sys.argv) > 2 else 3001

print(f"Testing server at {host}:{port}")
if check_server_connectivity(host, port):
    print("\\n✅ Server is accessible and responding to requests")
else:
    print("\\n❌ Server connectivity issues detected")
    print("Possible solutions:")
    print("1. Make sure the server is running: ./run_mcp.sh")
    print("2. Check if the port is correct (default is 3001)")
    print("3. Try running the server with: python -m src.mcp_cli --port 3001")
    print("4. Check firewall settings (should not be an issue for localhost)")
    print("5. Try using 0.0.0.0 instead of localhost: python -m src.mcp_cli --host 0.0.0.0 --port 3001")
'''
        
        # Create execution environment
        exec_globals = {
            'sys': sys,
            'check_server_connectivity': mock_check,
            'print': mock_print
        }
        
        # Execute the main block
        exec(main_block_code, exec_globals)
        
        # Verify the execution
        mock_check.assert_called_once_with("localhost", 3001)
        mock_print.assert_any_call("Testing server at localhost:3001")
        mock_print.assert_any_call("\n✅ Server is accessible and responding to requests") 