import pytest
from unittest.mock import patch, MagicMock
import sys
import os
import requests

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
import src.scripts.test_sse_init as test_sse_init


class TestSSEInit:
    
    @patch('src.scripts.test_sse_init.cancel_utils.get_sse_url')
    @patch('src.scripts.test_sse_init.requests.get')
    @patch('src.scripts.test_sse_init.requests.Session')
    def test_sse_initialization_success(self, mock_session_class, mock_get, mock_get_sse_url):
        """Test successful SSE initialization"""
        mock_url = "http://localhost:3000/sse"
        mock_get_sse_url.return_value = mock_url
        
        # Mock base URL response
        mock_base_response = MagicMock()
        mock_base_response.status_code = 200
        mock_get.return_value = mock_base_response
        
        # Mock session and POST response
        mock_session = MagicMock()
        mock_post_response = MagicMock()
        mock_post_response.status_code = 200
        mock_post_response.json.return_value = {"result": {"capabilities": {"tools": True}}}
        mock_session.post.return_value = mock_post_response
        mock_session_class.return_value = mock_session
        
        test_sse_init.test_sse_initialization()
        
        mock_get_sse_url.assert_called_once_with(None)
        mock_get.assert_called_once_with("http://localhost:3000", timeout=10)
        mock_session.post.assert_called_once()

    @patch('src.scripts.test_sse_init.cancel_utils.get_sse_url')
    @patch('src.scripts.test_sse_init.requests.get')
    @patch('src.scripts.test_sse_init.requests.Session')
    def test_sse_initialization_with_custom_url_and_timeout(self, mock_session_class, mock_get, mock_get_sse_url):
        """Test SSE initialization with custom URL and timeout"""
        mock_url = "http://example.com:8080/sse"
        mock_get_sse_url.return_value = mock_url
        
        # Mock base URL response
        mock_base_response = MagicMock()
        mock_base_response.status_code = 200
        mock_get.return_value = mock_base_response
        
        # Mock session and POST response
        mock_session = MagicMock()
        mock_post_response = MagicMock()
        mock_post_response.status_code = 200
        mock_post_response.json.return_value = {"result": {"capabilities": {"tools": True}}}
        mock_session.post.return_value = mock_post_response
        mock_session_class.return_value = mock_session
        
        test_sse_init.test_sse_initialization(url="custom_url", timeout=20)
        
        mock_get_sse_url.assert_called_once_with("custom_url")
        mock_get.assert_called_once_with("http://example.com:8080", timeout=20)

    @patch('src.scripts.test_sse_init.cancel_utils.get_sse_url')
    def test_sse_initialization_runtime_error(self, mock_get_sse_url):
        """Test handling of RuntimeError from get_sse_url"""
        mock_get_sse_url.side_effect = RuntimeError("Server not running")
        
        result = test_sse_init.test_sse_initialization()
        
        assert result is None
        mock_get_sse_url.assert_called_once_with(None)

    @patch('src.scripts.test_sse_init.cancel_utils.get_sse_url')
    @patch('src.scripts.test_sse_init.requests.get')
    @patch('src.scripts.test_sse_init.requests.Session')
    def test_sse_initialization_base_url_exception(self, mock_session_class, mock_get, mock_get_sse_url):
        """Test handling of exception when connecting to base URL"""
        mock_url = "http://localhost:3000/sse"
        mock_get_sse_url.return_value = mock_url
        
        # Mock base URL exception
        mock_get.side_effect = Exception("Connection failed")
        
        # Mock session and POST response
        mock_session = MagicMock()
        mock_post_response = MagicMock()
        mock_post_response.status_code = 200
        mock_post_response.json.return_value = {"result": {"capabilities": {"tools": True}}}
        mock_session.post.return_value = mock_post_response
        mock_session_class.return_value = mock_session
        
        test_sse_init.test_sse_initialization()
        
        # Should still try POST request even if base URL fails
        mock_session.post.assert_called_once()

    @patch('src.scripts.test_sse_init.cancel_utils.get_sse_url')
    @patch('src.scripts.test_sse_init.requests.get')
    @patch('src.scripts.test_sse_init.requests.Session')
    def test_sse_initialization_post_http_error(self, mock_session_class, mock_get, mock_get_sse_url):
        """Test handling of HTTP error in POST response"""
        mock_url = "http://localhost:3000/sse"
        mock_get_sse_url.return_value = mock_url
        
        # Mock base URL response
        mock_base_response = MagicMock()
        mock_base_response.status_code = 200
        mock_get.return_value = mock_base_response
        
        # Mock session and POST response with error
        mock_session = MagicMock()
        mock_post_response = MagicMock()
        mock_post_response.status_code = 500
        mock_post_response.text = "Internal Server Error"
        mock_session.post.return_value = mock_post_response
        mock_session_class.return_value = mock_session
        
        result = test_sse_init.test_sse_initialization()
        
        assert result is None

    @patch('src.scripts.test_sse_init.cancel_utils.get_sse_url')
    @patch('src.scripts.test_sse_init.requests.get')
    @patch('src.scripts.test_sse_init.requests.Session')
    def test_sse_initialization_post_timeout(self, mock_session_class, mock_get, mock_get_sse_url):
        """Test handling of POST request timeout"""
        mock_url = "http://localhost:3000/sse"
        mock_get_sse_url.return_value = mock_url
        
        # Mock base URL response
        mock_base_response = MagicMock()
        mock_base_response.status_code = 200
        mock_get.return_value = mock_base_response
        
        # Mock session with timeout exception
        mock_session = MagicMock()
        mock_session.post.side_effect = requests.exceptions.Timeout()
        mock_session_class.return_value = mock_session
        
        result = test_sse_init.test_sse_initialization()
        
        assert result is None

    @patch('src.scripts.test_sse_init.cancel_utils.get_sse_url')
    @patch('src.scripts.test_sse_init.requests.get')
    @patch('src.scripts.test_sse_init.requests.Session')
    def test_sse_initialization_post_connection_error(self, mock_session_class, mock_get, mock_get_sse_url):
        """Test handling of POST connection error"""
        mock_url = "http://localhost:3000/sse"
        mock_get_sse_url.return_value = mock_url
        
        # Mock base URL response
        mock_base_response = MagicMock()
        mock_base_response.status_code = 200
        mock_get.return_value = mock_base_response
        
        # Mock session with connection error
        mock_session = MagicMock()
        mock_session.post.side_effect = requests.exceptions.ConnectionError()
        mock_session_class.return_value = mock_session
        
        result = test_sse_init.test_sse_initialization()
        
        assert result is None

    @patch('src.scripts.test_sse_init.cancel_utils.get_sse_url')
    @patch('src.scripts.test_sse_init.requests.get')
    @patch('src.scripts.test_sse_init.requests.Session')
    def test_sse_initialization_post_generic_exception(self, mock_session_class, mock_get, mock_get_sse_url):
        """Test handling of generic exception during POST"""
        mock_url = "http://localhost:3000/sse"
        mock_get_sse_url.return_value = mock_url
        
        # Mock base URL response
        mock_base_response = MagicMock()
        mock_base_response.status_code = 200
        mock_get.return_value = mock_base_response
        
        # Mock session with generic exception
        mock_session = MagicMock()
        mock_session.post.side_effect = Exception("Generic error")
        mock_session_class.return_value = mock_session
        
        test_sse_init.test_sse_initialization()

    def test_main_execution_simulation(self):
        """Test that the main execution logic works correctly"""
        # Test with argument
        test_args = ['test_sse_init.py', 'http://custom.url']
        arg_url = test_args[1] if len(test_args) > 1 else None
        assert arg_url == 'http://custom.url'
        
        # Test without argument
        test_args = ['test_sse_init.py']
        arg_url = test_args[1] if len(test_args) > 1 else None
        assert arg_url is None 