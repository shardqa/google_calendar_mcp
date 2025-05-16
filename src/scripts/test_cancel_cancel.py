import sys
import requests
import json
import src.cancel_utils as cancel_utils

def test_cancel_request(url=None, timeout=10):
    try:
        url = cancel_utils.get_sse_url(url)
    except RuntimeError as e:
        print(str(e))
        return
    cancel_data = {
        "method": "mcp/cancel",
        "params": {},
        "jsonrpc": "2.0",
        "id": 1
    }
    print(f"Sending cancel request to {url}")
    try:
        session = requests.Session()
        session.keep_alive = False
        headers = {"Content-Type": "application/json", "Connection": "close"}
        response = session.post(url, json=cancel_data, timeout=timeout, headers=headers)
        print(f"Cancel request status: {response.status_code}")
        if response.status_code != 200:
            print(f"Error: Cancel request failed with status code {response.status_code}")
            print(response.text)
            return
        print(f"Cancel response: {response.json()}")
        result = response.json()
        if "result" in result and "cancelled" in result["result"] and result["result"]["cancelled"] == True:
            print("✅ Success: Server correctly responded to cancellation request")
        else:
            print("❌ Error: Server did not respond with proper cancellation format")
    except requests.exceptions.Timeout:
        print(f"Error: Cancel request timed out after {timeout} seconds")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to server for cancel request")
    except Exception as e:
        print(f"Error during cancel request: {str(e)}")

if __name__ == "__main__":
    arg_url = sys.argv[1] if len(sys.argv) > 1 else None
    test_cancel_request(arg_url) 