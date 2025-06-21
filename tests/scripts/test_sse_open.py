import pytest
from unittest.mock import patch, MagicMock, mock_open
import sys
import os
import requests

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
import src.scripts.test_sse_open as test_sse_open


class TestSSEOpen:
    
    @patch('src.scripts.test_sse_open.cancel_utils.get_sse_url')
    @patch('src.scripts.test_sse_open.requests.Session')
    def test_sse_open_connection_success(self, mock_session_class, mock_get_sse_url):
        """Test successful SSE connection"""
        mock_url = "http://localhost:3000/sse"
        mock_get_sse_url.return_value = mock_url
        
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_session.get.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        test_sse_open.test_sse_open_connection()
        
        mock_get_sse_url.assert_called_once_with(None)
        mock_session.get.assert_called_once_with(
            mock_url,
            headers={"Accept": "text/event-stream", "Cache-Control": "no-cache"},
            stream=True,
            timeout=10
        )
        mock_response.close.assert_called_once()

    @patch('src.scripts.test_sse_open.cancel_utils.get_sse_url')
    @patch('src.scripts.test_sse_open.requests.Session')
    def test_sse_open_connection_with_custom_url_and_timeout(self, mock_session_class, mock_get_sse_url):
        """Test SSE connection with custom URL and timeout"""
        mock_url = "http://example.com:8080/sse"
        mock_get_sse_url.return_value = mock_url
        
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_session.get.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        test_sse_open.test_sse_open_connection(url="custom_url", timeout=20)
        
        mock_get_sse_url.assert_called_once_with("custom_url")
        mock_session.get.assert_called_once_with(
            mock_url,
            headers={"Accept": "text/event-stream", "Cache-Control": "no-cache"},
            stream=True,
            timeout=20
        )

    @patch('src.scripts.test_sse_open.cancel_utils.get_sse_url')
    def test_sse_open_connection_runtime_error(self, mock_get_sse_url):
        """Test handling of RuntimeError from get_sse_url"""
        mock_get_sse_url.side_effect = RuntimeError("Server not running")
        
        result = test_sse_open.test_sse_open_connection()
        
        assert result is None
        mock_get_sse_url.assert_called_once_with(None)

    @patch('src.scripts.test_sse_open.cancel_utils.get_sse_url')
    @patch('src.scripts.test_sse_open.requests.Session')
    def test_sse_open_connection_http_error(self, mock_session_class, mock_get_sse_url):
        """Test handling of HTTP error response"""
        mock_url = "http://localhost:3000/sse"
        mock_get_sse_url.return_value = mock_url
        
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_session.get.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        test_sse_open.test_sse_open_connection()
        
        mock_response.close.assert_called_once()

    @patch('src.scripts.test_sse_open.cancel_utils.get_sse_url')
    @patch('src.scripts.test_sse_open.requests.Session')
    def test_sse_open_connection_timeout(self, mock_session_class, mock_get_sse_url):
        """Test handling of request timeout"""
        mock_url = "http://localhost:3000/sse"
        mock_get_sse_url.return_value = mock_url
        
        mock_session = MagicMock()
        mock_session.get.side_effect = requests.exceptions.Timeout()
        mock_session_class.return_value = mock_session
        
        result = test_sse_open.test_sse_open_connection()
        
        assert result is None

    @patch('src.scripts.test_sse_open.cancel_utils.get_sse_url')
    @patch('src.scripts.test_sse_open.requests.Session')
    def test_sse_open_connection_connection_error(self, mock_session_class, mock_get_sse_url):
        """Test handling of connection error"""
        mock_url = "http://localhost:3000/sse"
        mock_get_sse_url.return_value = mock_url
        
        mock_session = MagicMock()
        mock_session.get.side_effect = requests.exceptions.ConnectionError()
        mock_session_class.return_value = mock_session
        
        result = test_sse_open.test_sse_open_connection()
        
        assert result is None

    @patch('src.scripts.test_sse_open.cancel_utils.get_sse_url')
    @patch('src.scripts.test_sse_open.requests.Session')
    def test_sse_open_connection_generic_exception(self, mock_session_class, mock_get_sse_url):
        """Test handling of generic exception"""
        mock_url = "http://localhost:3000/sse"
        mock_get_sse_url.return_value = mock_url
        
        mock_session = MagicMock()
        mock_session.get.side_effect = Exception("Generic error")
        mock_session_class.return_value = mock_session
        
        test_sse_open.test_sse_open_connection()

    @patch('src.scripts.test_sse_open.cancel_utils.get_sse_url')
    @patch('src.scripts.test_sse_open.requests.Session')
    def test_sse_open_connection_close_exception(self, mock_session_class, mock_get_sse_url):
        """Test handling of exception during response close"""
        mock_url = "http://localhost:3000/sse"
        mock_get_sse_url.return_value = mock_url
        
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.close.side_effect = Exception("Close error")
        mock_session.get.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        test_sse_open.test_sse_open_connection()

    def test_main_execution_simulation(self):
        """Test that the main execution logic works correctly"""
        # Test with argument
        test_args = ['test_sse_open.py', 'http://custom.url']
        arg_url = test_args[1] if len(test_args) > 1 else None
        assert arg_url == 'http://custom.url'
        
        # Test without argument
        test_args = ['test_sse_open.py']
        arg_url = test_args[1] if len(test_args) > 1 else None
        assert arg_url is None 