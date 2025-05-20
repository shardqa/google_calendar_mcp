import pytest
from unittest.mock import patch, MagicMock
import requests
import json
import src.scripts.test_cancel_cancel as script_mod

# Define a dummy URL to use in tests
DUMMY_URL = "http://dummy-server/sse"

# Helper to create a mock response object
def create_mock_response(status_code, json_data=None, text=None):
    mock_response = MagicMock()
    mock_response.status_code = status_code
    if json_data is not None:
        mock_response.json.return_value = json_data
    if text is not None:
         mock_response.text = text
    else:
         # Provide a default text attribute to avoid AttributeError if .text is accessed
         mock_response.text = ""
    return mock_response

@patch('src.core.cancel_utils.get_sse_url')
@patch('requests.Session')
def test_cancel_request_success(mock_session_class, mock_get_sse_url, capsys):
    # Mock get_sse_url to return a dummy URL
    mock_get_sse_url.return_value = DUMMY_URL

    # Mock the requests.Session and its post method
    mock_session_instance = MagicMock()
    mock_session_class.return_value = mock_session_instance
    
    # Mock the post response for success
    success_response_data = {"jsonrpc": "2.0", "result": {"cancelled": True}}
    mock_post_response = create_mock_response(200, json_data=success_response_data)
    mock_session_instance.post.return_value = mock_post_response

    # Call the function under test
    script_mod.test_cancel_request(url=None) # Pass url=None to trigger get_sse_url call

    # Assertions
    mock_get_sse_url.assert_called_once_with(None)
    mock_session_class.assert_called_once()
    mock_session_instance.post.assert_called_once_with(
        DUMMY_URL,
        json={
            "method": "mcp/cancel",
            "params": {},
            "jsonrpc": "2.0",
            "id": 1
        },
        timeout=10,
        headers={"Content-Type": "application/json", "Connection": "close"}
    )
    mock_post_response.json.assert_called_once()
    
    # Capture stdout and assert success message
    captured = capsys.readouterr()
    assert "✅ Success: Server correctly responded to cancellation request" in captured.out

@patch('src.core.cancel_utils.get_sse_url')
@patch('requests.Session')
def test_cancel_request_get_url_error(mock_session_class, mock_get_sse_url, capsys):
    # Mock get_sse_url to raise a RuntimeError
    mock_get_sse_url.side_effect = RuntimeError("fake url error")

    # Call the function under test
    script_mod.test_cancel_request(url=None) # Pass url=None to trigger get_sse_url call

    # Assertions
    mock_get_sse_url.assert_called_once_with(None)
    mock_session_class.assert_not_called() # Ensure no session is created

    # Capture stdout and assert error message
    captured = capsys.readouterr()
    assert "fake url error" in captured.out

@patch('src.core.cancel_utils.get_sse_url')
@patch('requests.Session')
def test_cancel_request_non_200_status(mock_session_class, mock_get_sse_url, capsys):
    mock_get_sse_url.return_value = DUMMY_URL

    mock_session_instance = MagicMock()
    mock_session_class.return_value = mock_session_instance
    
    # Mock the post response for non-200 status
    error_text = "Internal Server Error"
    mock_post_response = create_mock_response(500, text=error_text)
    mock_session_instance.post.return_value = mock_post_response

    script_mod.test_cancel_request(url=None)

    mock_get_sse_url.assert_called_once_with(None)
    mock_session_instance.post.assert_called_once()
    
    # Capture stdout and assert error message
    captured = capsys.readouterr()
    assert "Error: Cancel request failed with status code 500" in captured.out
    assert error_text in captured.out

@patch('src.core.cancel_utils.get_sse_url')
@patch('requests.Session')
def test_cancel_request_timeout_error(mock_session_class, mock_get_sse_url, capsys):
    mock_get_sse_url.return_value = DUMMY_URL

    mock_session_instance = MagicMock()
    mock_session_class.return_value = mock_session_instance
    
    # Mock the post method to raise a Timeout exception
    mock_session_instance.post.side_effect = requests.exceptions.Timeout("fake timeout error")

    script_mod.test_cancel_request(url=None)

    mock_get_sse_url.assert_called_once_with(None)
    mock_session_instance.post.assert_called_once()
    
    # Capture stdout and assert error message
    captured = capsys.readouterr()
    assert "Error: Cancel request timed out after 10 seconds" in captured.out

@patch('src.core.cancel_utils.get_sse_url')
@patch('requests.Session')
def test_cancel_request_connection_error(mock_session_class, mock_get_sse_url, capsys):
    mock_get_sse_url.return_value = DUMMY_URL

    mock_session_instance = MagicMock()
    mock_session_class.return_value = mock_session_instance
    
    # Mock the post method to raise a ConnectionError exception
    mock_session_instance.post.side_effect = requests.exceptions.ConnectionError("fake connection error")

    script_mod.test_cancel_request(url=None)

    mock_get_sse_url.assert_called_once_with(None)
    mock_session_instance.post.assert_called_once()
    
    # Capture stdout and assert error message
    captured = capsys.readouterr()
    assert "Error: Could not connect to server for cancel request" in captured.out

@patch('src.core.cancel_utils.get_sse_url')
@patch('requests.Session')
def test_cancel_request_other_exception(mock_session_class, mock_get_sse_url, capsys):
    mock_get_sse_url.return_value = DUMMY_URL

    mock_session_instance = MagicMock()
    mock_session_class.return_value = mock_session_instance
    
    # Mock the post method to raise a generic Exception
    mock_session_instance.post.side_effect = Exception("fake other error")

    script_mod.test_cancel_request(url=None)

    mock_get_sse_url.assert_called_once_with(None)
    mock_session_instance.post.assert_called_once()
    
    # Capture stdout and assert error message
    captured = capsys.readouterr()
    assert "Error during cancel request: fake other error" in captured.out

@patch('src.core.cancel_utils.get_sse_url')
@patch('requests.Session')
def test_cancel_request_incorrect_response_format(mock_session_class, mock_get_sse_url, capsys):
    mock_get_sse_url.return_value = DUMMY_URL

    mock_session_instance = MagicMock()
    mock_session_class.return_value = mock_session_instance
    
    # Mock the post response with incorrect format
    incorrect_response_data = {"status": "ok"}
    mock_post_response = create_mock_response(200, json_data=incorrect_response_data)
    mock_session_instance.post.return_value = mock_post_response

    script_mod.test_cancel_request(url=None)

    mock_get_sse_url.assert_called_once_with(None)
    mock_session_instance.post.assert_called_once()
    mock_post_response.json.assert_called_once()
    
    # Capture stdout and assert error message
    captured = capsys.readouterr()
    assert "❌ Error: Server did not respond with proper cancellation format" in captured.out

@patch('src.core.cancel_utils.get_sse_url')
@patch('requests.Session')
def test_cancel_request_server_not_cancelled(mock_session_class, mock_get_sse_url, capsys):
    mock_get_sse_url.return_value = DUMMY_URL

    mock_session_instance = MagicMock()
    mock_session_class.return_value = mock_session_instance
    
    # Mock the post response indicating not cancelled
    not_cancelled_response_data = {"jsonrpc": "2.0", "result": {"cancelled": False}}
    mock_post_response = create_mock_response(200, json_data=not_cancelled_response_data)
    mock_session_instance.post.return_value = mock_post_response

    script_mod.test_cancel_request(url=None)

    mock_get_sse_url.assert_called_once_with(None)
    mock_session_instance.post.assert_called_once()
    mock_post_response.json.assert_called_once()
    
    # Capture stdout and assert error message
    captured = capsys.readouterr()
    assert "❌ Error: Server did not respond with proper cancellation format" in captured.out 