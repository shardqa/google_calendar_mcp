import sys
import requests
import src.core.cancel_utils as cancel_utils

def test_sse_open_connection(url=None, timeout=10):
    try:
        url = cancel_utils.get_sse_url(url)
    except RuntimeError as e:
        print(str(e))
        return
    print(f"Opening SSE connection to {url}")
    headers = {"Accept": "text/event-stream", "Cache-Control": "no-cache"}
    try:
        get_session = requests.Session()
        sse_response = get_session.get(url, headers=headers, stream=True, timeout=timeout)
        print(f"SSE connection status: {sse_response.status_code}")
        if sse_response.status_code != 200:
            print(f"Error: SSE connection failed with status code {sse_response.status_code}")
            print(sse_response.text)
        else:
            print("SSE connection established successfully")
    except requests.exceptions.Timeout:
        print(f"Error: SSE connection timed out after {timeout} seconds")
        return
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to server for SSE. Is the server running?")
        return
    except Exception as e:
        print(f"Error establishing SSE connection: {str(e)}")
    finally:
        try:
            sse_response.close()
        except:
            pass

if __name__ == "__main__":
    arg_url = sys.argv[1] if len(sys.argv) > 1 else None
    test_sse_open_connection(arg_url) 