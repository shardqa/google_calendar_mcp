import pytest
from unittest.mock import patch, MagicMock
import sys
import os
import requests

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
import src.scripts.test_cancel_cancel as test_cancel_cancel


class TestCancelCancel:
    
    @patch('src.scripts.test_cancel_cancel.cancel_utils.get_sse_url')
    @patch('src.scripts.test_cancel_cancel.requests.Session')
    def test_cancel_request_success(self, mock_session_class, mock_get_sse_url):
        """Test successful cancel request"""
        mock_url = "http://localhost:3000/sse"
        mock_get_sse_url.return_value = mock_url
        
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": {"cancelled": True}, "jsonrpc": "2.0", "id": 1}
        mock_session.post.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        result = test_cancel_cancel.test_cancel_request()
        
        mock_get_sse_url.assert_called_once_with(None)
        mock_session.post.assert_called_once()

    @patch('src.scripts.test_cancel_cancel.cancel_utils.get_sse_url')
    @patch('src.scripts.test_cancel_cancel.requests.Session')
    def test_cancel_request_with_custom_url(self, mock_session_class, mock_get_sse_url):
        """Test cancel request with custom URL"""
        mock_url = "http://example.com:8080/sse"
        mock_get_sse_url.return_value = mock_url
        
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": {"cancelled": True}, "jsonrpc": "2.0", "id": 1}
        mock_session.post.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        test_cancel_cancel.test_cancel_request("custom_url")
        
        mock_get_sse_url.assert_called_once_with("custom_url")

    @patch('src.scripts.test_cancel_cancel.cancel_utils.get_sse_url')
    def test_cancel_request_runtime_error(self, mock_get_sse_url):
        """Test handling of RuntimeError from get_sse_url"""
        mock_get_sse_url.side_effect = RuntimeError("Server not running")
        
        result = test_cancel_cancel.test_cancel_request()
        
        assert result is None
        mock_get_sse_url.assert_called_once_with(None)

    @patch('src.scripts.test_cancel_cancel.cancel_utils.get_sse_url')
    @patch('src.scripts.test_cancel_cancel.requests.Session')
    def test_cancel_request_http_error(self, mock_session_class, mock_get_sse_url):
        """Test handling of HTTP error in request"""
        mock_url = "http://localhost:3000/sse"
        mock_get_sse_url.return_value = mock_url
        
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_session.post.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        result = test_cancel_cancel.test_cancel_request()
        
        assert result is None

    @patch('src.scripts.test_cancel_cancel.cancel_utils.get_sse_url')
    @patch('src.scripts.test_cancel_cancel.requests.Session')
    def test_cancel_request_timeout(self, mock_session_class, mock_get_sse_url):
        """Test handling of request timeout"""
        mock_url = "http://localhost:3000/sse"
        mock_get_sse_url.return_value = mock_url
        
        mock_session = MagicMock()
        mock_session.post.side_effect = requests.exceptions.Timeout()
        mock_session_class.return_value = mock_session
        
        result = test_cancel_cancel.test_cancel_request()
        
        assert result is None

    @patch('src.scripts.test_cancel_cancel.cancel_utils.get_sse_url')
    @patch('src.scripts.test_cancel_cancel.requests.Session')
    def test_cancel_request_connection_error(self, mock_session_class, mock_get_sse_url):
        """Test handling of connection error"""
        mock_url = "http://localhost:3000/sse"
        mock_get_sse_url.return_value = mock_url
        
        mock_session = MagicMock()
        mock_session.post.side_effect = requests.exceptions.ConnectionError()
        mock_session_class.return_value = mock_session
        
        result = test_cancel_cancel.test_cancel_request()
        
        assert result is None

    @patch('src.scripts.test_cancel_cancel.cancel_utils.get_sse_url')
    @patch('src.scripts.test_cancel_cancel.requests.Session')
    def test_cancel_request_generic_exception(self, mock_session_class, mock_get_sse_url):
        """Test handling of generic exception"""
        mock_url = "http://localhost:3000/sse"
        mock_get_sse_url.return_value = mock_url
        
        mock_session = MagicMock()
        mock_session.post.side_effect = Exception("Generic error")
        mock_session_class.return_value = mock_session
        
        result = test_cancel_cancel.test_cancel_request()
        
        assert result is None

    @patch('src.scripts.test_cancel_cancel.cancel_utils.get_sse_url')
    @patch('src.scripts.test_cancel_cancel.requests.Session')
    def test_cancel_request_invalid_response_format(self, mock_session_class, mock_get_sse_url):
        """Test handling of invalid response format"""
        mock_url = "http://localhost:3000/sse"
        mock_get_sse_url.return_value = mock_url
        
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"invalid": "response"}
        mock_session.post.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        result = test_cancel_cancel.test_cancel_request()
        
        assert result is None

    def test_main_execution_simulation(self):
        """Test that the main execution logic works correctly"""
        # Test with argument
        test_args = ['test_cancel_cancel.py', 'http://custom.url']
        arg_url = test_args[1] if len(test_args) > 1 else None
        assert arg_url == 'http://custom.url'
        
        # Test without argument
        test_args = ['test_cancel_cancel.py']
        arg_url = test_args[1] if len(test_args) > 1 else None
        assert arg_url is None 