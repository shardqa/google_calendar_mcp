import threading
import time
import pytest
from src.mcp.mcp_server import CalendarMCPServer, run_server
import src.mcp.mcp_server as mcp_server_module
from unittest.mock import patch, MagicMock
import socket

@patch('src.mcp.mcp_server.ThreadingHTTPServer')
@patch('src.mcp.mcp_server.CalendarMCPHandler')
class TestCalendarMCPServer:

    def test_init_localhost(self, MockHandler, MockHTTPServer):
        server = CalendarMCPServer(host="localhost", port=8000)
        MockHTTPServer.assert_called_once_with(("0.0.0.0", 8000), MockHandler)
        assert server.host == "localhost"
        assert server.port == 8000
        assert server.running is False
        assert server.server_thread is None
        # Mock socket and setsockopt
        mock_socket = MagicMock()
        MockHTTPServer.return_value.socket = mock_socket
        server = CalendarMCPServer(host="localhost", port=8000)
        mock_socket.setsockopt.assert_called_once_with(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def test_init_specific_host(self, MockHandler, MockHTTPServer):
        server = CalendarMCPServer(host="192.168.1.100", port=8080)
        MockHTTPServer.assert_called_once_with(("192.168.1.100", 8080), MockHandler)
        assert server.host == "192.168.1.100"
        assert server.port == 8080
        assert server.running is False
        assert server.server_thread is None
        # Mock socket and setsockopt
        mock_socket = MagicMock()
        MockHTTPServer.return_value.socket = mock_socket
        server = CalendarMCPServer(host="192.168.1.100", port=8080)
        mock_socket.setsockopt.assert_called_once_with(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    @patch('src.mcp.mcp_server.threading.Thread')
    def test_start_server(self, MockThread, MockHandler, MockHTTPServer):
        server = CalendarMCPServer()
        mock_server_instance = MockHTTPServer.return_value
        mock_thread_instance = MockThread.return_value

        server.start()

        assert server.running is True
        MockThread.assert_called_once_with(target=mock_server_instance.serve_forever)
        mock_thread_instance.daemon = True
        mock_thread_instance.start.assert_called_once()

    def test_stop_server(self, MockHandler, MockHTTPServer):
        server = CalendarMCPServer()
        server.running = True
        server.server_thread = MagicMock(spec=threading.Thread)
        mock_server_instance = MockHTTPServer.return_value
        server.server = mock_server_instance

        server.stop()

        assert server.running is False
        mock_server_instance.shutdown.assert_called_once()
        server.server_thread.join.assert_called_once()

    def test_start_when_already_running(self, MockHandler, MockHTTPServer):
        server = CalendarMCPServer()
        server.running = True

        with patch('src.mcp.mcp_server.threading.Thread') as MockThread:
            server.start()
            MockThread.assert_not_called()

    def test_stop_when_not_running(self, MockHandler, MockHTTPServer):
        server = CalendarMCPServer()
        server.running = False
        mock_server_instance = MockHTTPServer.return_value
        server.server = mock_server_instance

        server.stop()

        mock_server_instance.shutdown.assert_not_called()

@patch('src.mcp.mcp_server.CalendarMCPServer')
@patch('src.mcp.mcp_server.time.sleep')
def test_run_server_keyboard_interrupt(mock_sleep, MockCalendarMCPServer):
    mock_server_instance = MockCalendarMCPServer.return_value
    mock_sleep.side_effect = KeyboardInterrupt

    run_server()

    mock_server_instance.start.assert_called_once()
    mock_sleep.assert_called_once_with(1)
    mock_server_instance.stop.assert_called_once() 