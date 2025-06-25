import pytest
from unittest.mock import MagicMock, patch
from src.mcp.mcp_post_handler import handle_post


def test_handle_post_sse_path():
    handler = MagicMock()
    handler.path = '/sse'
    request = {'method': 'test'}
    response = {}
    
    with patch('src.mcp.mcp_post_handler.handle_post_sse') as mock_sse:
        handle_post(handler, request, response)
        mock_sse.assert_called_once_with(handler, request, response)


def test_handle_post_other_path():
    handler = MagicMock()
    handler.path = '/other'
    request = {'method': 'test'}
    response = {}
    
    with patch('src.mcp.mcp_post_handler.handle_post_other') as mock_other:
        handle_post(handler, request, response)
        mock_other.assert_called_once_with(handler, request, response)


def test_handle_post_default_path():
    handler = MagicMock()
    handler.path = '/'
    request = {'method': 'test'}
    response = {}
    
    with patch('src.mcp.mcp_post_handler.handle_post_other') as mock_other:
        handle_post(handler, request, response)
        mock_other.assert_called_once_with(handler, request, response) 