import pytest
import socket
from unittest.mock import patch, MagicMock
from src.core.cancel_utils import check_server_status, get_sse_url


def test_check_server_status_success():
    with patch('socket.socket') as mock_socket:
        mock_sock = MagicMock()
        mock_socket.return_value = mock_sock
        mock_sock.connect_ex.return_value = 0
        
        result = check_server_status('localhost', 3000)
        
        assert result is True
        mock_sock.settimeout.assert_called_once_with(2)
        mock_sock.connect_ex.assert_called_once_with(('localhost', 3000))
        mock_sock.close.assert_called_once()


def test_check_server_status_connection_failed():
    with patch('socket.socket') as mock_socket:
        mock_sock = MagicMock()
        mock_socket.return_value = mock_sock
        mock_sock.connect_ex.return_value = 1
        
        result = check_server_status('localhost', 3000)
        
        assert result is False


def test_check_server_status_exception():
    with patch('socket.socket') as mock_socket:
        mock_socket.side_effect = Exception('Socket error')
        
        result = check_server_status('localhost', 3000)
        
        assert result is False


def test_check_server_status_custom_timeout():
    with patch('socket.socket') as mock_socket:
        mock_sock = MagicMock()
        mock_socket.return_value = mock_sock
        mock_sock.connect_ex.return_value = 0
        
        result = check_server_status('localhost', 3000, timeout=5)
        
        mock_sock.settimeout.assert_called_once_with(5)


def test_get_sse_url_with_provided_url():
    result = get_sse_url(url='http://custom:8080/sse')
    assert result == 'http://custom:8080/sse'


def test_get_sse_url_default_ports_first_available():
    with patch('src.core.cancel_utils.check_server_status') as mock_check:
        mock_check.side_effect = [True, False]
        
        result = get_sse_url()
        
        assert result == 'http://localhost:3001/sse'
        mock_check.assert_called_with('localhost', 3001)


def test_get_sse_url_default_ports_second_available():
    with patch('src.core.cancel_utils.check_server_status') as mock_check:
        mock_check.side_effect = [False, True]
        
        result = get_sse_url()
        
        assert result == 'http://localhost:3000/sse'
        assert mock_check.call_count == 2


def test_get_sse_url_custom_ports():
    with patch('src.core.cancel_utils.check_server_status') as mock_check:
        mock_check.side_effect = [False, True]
        
        result = get_sse_url(ports_to_try=[8080, 8081])
        
        assert result == 'http://localhost:8081/sse'


def test_get_sse_url_custom_host():
    with patch('src.core.cancel_utils.check_server_status') as mock_check:
        mock_check.return_value = True
        
        result = get_sse_url(host='example.com')
        
        assert result == 'http://example.com:3001/sse'
        mock_check.assert_called_with('example.com', 3001)


def test_get_sse_url_no_server_available():
    with patch('src.core.cancel_utils.check_server_status') as mock_check:
        mock_check.return_value = False
        
        with pytest.raises(RuntimeError, match='No server detected on common ports'):
            get_sse_url() 