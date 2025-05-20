import unittest
from unittest.mock import patch, MagicMock
from src.mcp.mcp_handler import CalendarMCPHandler
import json
from http.server import BaseHTTPRequestHandler
from http.client import HTTPMessage

class TestCalendarMCPHandler(unittest.TestCase):

    @patch('http.server.BaseHTTPRequestHandler.__init__')
    def setUp(self, mock_base_init):
        # Mock the __init__ of the base class to do nothing
        mock_base_init.return_value = None

        # Create mocks for the arguments passed to CalendarMCPHandler's __init__
        mock_request = MagicMock()
        mock_client_address = ('127.0.0.1', 12345)
        mock_server = MagicMock()

        # Instantiate our handler (BaseHTTPRequestHandler.__init__ is mocked)
        self.handler = CalendarMCPHandler(mock_request, mock_client_address, mock_server)

        # Manually set the essential attributes that BaseHTTPRequestHandler.__init__ would normally set,
        # using mocks and simulated values.
        self.handler.request = mock_request
        self.handler.client_address = mock_client_address
        self.handler.server = mock_server

        # Mock the file-like objects for reading request body and writing response body
        self.handler.rfile = MagicMock() # Request input stream
        self.handler.wfile = MagicMock() # Response output stream

        # Mock methods for sending response and headers
        self.handler.send_response = MagicMock()
        self.handler.send_header = MagicMock()
        self.handler.end_headers = MagicMock()

        # Mock the headers attribute
        # mock_headers = HTTPMessage()
        # mock_headers['Content-Length'] = '0' # Default Content-Length
        self.handler.headers = MagicMock() # Use MagicMock for more control

        # Simulate request line attributes normally set by parse_request
        self.handler.command = 'GET' # Default command
        self.handler.path = '/sse' # Set path to /sse to trigger handle_get logic
        self.handler.request_version = 'HTTP/1.1' # Default version
        # Ensure raw_requestline is explicitly set as bytes
        self.handler.raw_requestline = b'GET /sse HTTP/1.1\r\n'

        # For POST tests, configure rfile.read to return empty bytes by default
        # Specific POST tests will override this to provide request body
        self.handler.rfile.read.return_value = b''

    def test_do_OPTIONS(self):
        # Call do_OPTIONS on the handler instance created in setUp
        self.handler.do_OPTIONS()

        self.handler.send_response.assert_called_once_with(200)
        self.handler.send_header.assert_any_call('Access-Control-Allow-Origin', '*')
        self.handler.send_header.assert_any_call('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.handler.send_header.assert_any_call('Access-Control-Allow-Headers', 'Content-Type')
        self.handler.end_headers.assert_called_once()

    @patch('src.mcp.mcp_handler.handle_get')
    def test_do_GET(self, mock_handle_get):
        # Call do_GET on the handler instance created in setUp
        self.handler.do_GET()

        # Verify handle_get was called with the handler instance
        mock_handle_get.assert_called_once_with(self.handler)

    @patch('src.mcp.mcp_handler.handle_post')
    @patch('json.loads')
    def test_do_POST_success(self, mock_json_loads, mock_handle_post):
        # Specific setup for this POST test on the handler instance from setUp
        request_body = {"jsonrpc": "2.0", "method": "test_method", "id": "1"}
        request_body_bytes = json.dumps(request_body).encode('utf-8')

        # Update headers and rfile for this specific request just before calling do_POST
        self.handler.headers.get.return_value = str(len(request_body_bytes))
        self.handler.rfile.read.return_value = request_body_bytes

        mock_json_loads.return_value = request_body

        # Call do_POST on the handler instance created in setUp
        self.handler.do_POST()

        # Assertions for successful POST
        self.handler.rfile.read.assert_called_once_with(len(request_body_bytes))
        mock_json_loads.assert_called_once_with(request_body_bytes.decode('utf-8'))
        mock_handle_post.assert_called_once()
        args, kwargs = mock_handle_post.call_args
        self.assertEqual(args[0], self.handler)
        self.assertEqual(args[1], request_body)
        self.assertIn("jsonrpc", args[2])
        self.assertIn("id", args[2])
        self.assertEqual(args[2]["jsonrpc"], request_body["jsonrpc"])
        self.assertEqual(args[2]["id"], request_body["id"])

    @patch('src.mcp.mcp_handler.handle_post')
    @patch('json.loads')
    def test_do_POST_json_decode_error(self, mock_json_loads, mock_handle_post):
        # Specific setup for this POST error test on the handler instance from setUp
        invalid_json_body_bytes = b'invalid json'

        # Update headers and rfile for this specific request just before calling do_POST
        self.handler.headers.get.return_value = str(len(invalid_json_body_bytes))
        self.handler.rfile.read.return_value = invalid_json_body_bytes

        mock_json_loads.side_effect = json.JSONDecodeError("Invalid JSON", "{}", 0)

        # Call do_POST on the handler instance created in setUp
        self.handler.do_POST()

        # Assertions for JSON decode error
        self.handler.rfile.read.assert_called_once_with(len(invalid_json_body_bytes))
        mock_json_loads.assert_called_once_with(invalid_json_body_bytes.decode('utf-8'))
        mock_handle_post.assert_not_called()

        self.handler.send_response.assert_called_once_with(400)
        self.handler.send_header.assert_any_call('Content-Type', 'application/json')
        self.handler.send_header.assert_any_call('Access-Control-Allow-Origin', '*')
        self.handler.send_header.assert_any_call('Connection', 'close')
        self.handler.end_headers.assert_called_once()

        expected_error_response = {"jsonrpc": "2.0", "error": {"code": -32700, "message": "Parse error"}, "id": None}
        self.handler.wfile.write.assert_called_once_with(json.dumps(expected_error_response).encode())

    @patch('src.mcp.mcp_handler.handle_post')
    @patch('json.loads')
    def test_do_POST_general_exception(self, mock_json_loads, mock_handle_post):
        # Specific setup for this general exception POST test on the handler instance from setUp
        request_body = {"jsonrpc": "2.0", "method": "test_method", "id": "1"}
        request_body_bytes = json.dumps(request_body).encode('utf-8')

        # Update headers and rfile for this specific request just before calling do_POST
        self.handler.headers.get.return_value = str(len(request_body_bytes))
        self.handler.rfile.read.return_value = request_body_bytes

        mock_json_loads.return_value = request_body
        mock_handle_post.side_effect = Exception("Internal Server Error")

        # Call do_POST on the handler instance created in setUp
        self.handler.do_POST()

        # Assertions for general exception in POST
        self.handler.rfile.read.assert_called_once_with(len(request_body_bytes))
        mock_json_loads.assert_called_once_with(request_body_bytes.decode('utf-8'))
        mock_handle_post.assert_called_once()

        self.handler.send_response.assert_called_once_with(500)
        self.handler.send_header.assert_any_call('Content-Type', 'application/json')
        self.handler.send_header.assert_any_call('Access-Control-Allow-Origin', '*')
        self.handler.send_header.assert_any_call('Connection', 'close')
        self.handler.end_headers.assert_called_once()

        expected_error_response = {"jsonrpc": "2.0", "error": {"code": -32000, "message": "Internal Server Error"}, "id": request_body["id"]}
        self.handler.wfile.write.assert_called_once_with(json.dumps(expected_error_response).encode()) 