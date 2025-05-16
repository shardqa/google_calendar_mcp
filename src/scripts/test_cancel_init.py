import sys
import requests
import json
import time
import src.core.cancel_utils as cancel_utils

def test_cancel_initialization(url=None, timeout=10):
    try:
        url = cancel_utils.get_sse_url(url)
    except RuntimeError as e:
        print(str(e))
        return
    print(f"Using URL: {url}")
    base_url = url.rsplit('/', 1)[0]
    try:
        print(f"Testing basic connectivity to {base_url}...")
        response = requests.get(base_url, timeout=timeout)
        print(f"Base URL connection successful: {response.status_code}")
    except Exception as e:
        print(f"Warning: Could not connect to base URL: {str(e)}")
        print("Will try the SSE endpoint directly anyway")
    init_data = {
        "method": "initialize",
        "params": {
            "protocolVersion": "2025-03-26",
            "capabilities": {
                "tools": True,
                "prompts": False,
                "resources": True,
                "logging": False,
                "roots": {"listChanged": False}
            },
            "clientInfo": {
                "name": "test-client",
                "version": "1.0.0"
            }
        },
        "jsonrpc": "2.0",
        "id": 0
    }
    print(f"Sending initialization POST request to {url}")
    try:
        session = requests.Session()
        session.keep_alive = False
        headers = {"Content-Type": "application/json", "Connection": "close"}
        response = session.post(url, json=init_data, timeout=timeout, headers=headers)
        print(f"POST request status: {response.status_code}")
        if response.status_code != 200:
            print(f"Error: POST request failed with status code {response.status_code}")
            print(response.text)
            return
        print(f"POST response: {response.json()}")
    except requests.exceptions.Timeout:
        print(f"Error: POST request timed out after {timeout} seconds")
        return
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to server. Is the server running?")
        print("Try manually accessing the URL in a browser to check connectivity.")
        return
    except Exception as e:
        print(f"Error during POST request: {str(e)}")
        return

if __name__ == "__main__":
    arg_url = sys.argv[1] if len(sys.argv) > 1 else None
    test_cancel_initialization(arg_url) 