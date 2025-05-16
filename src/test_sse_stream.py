import sys
import time
import json
import requests
import src.cancel_utils as cancel_utils

def test_sse_stream_read(url=None, timeout=10, event_timeout=20):
    try:
        url = cancel_utils.get_sse_url(url)
    except RuntimeError as e:
        print(str(e))
        return
    headers = {"Accept": "text/event-stream", "Cache-Control": "no-cache"}
    try:
        get_session = requests.Session()
        sse_response = get_session.get(url, headers=headers, stream=True, timeout=timeout)
        print(f"SSE stream status: {sse_response.status_code}")
        if sse_response.status_code != 200:
            print(f"Error: Unexpected status code {sse_response.status_code}")
            return
        print("SSE stream open, waiting for events")
    except Exception as e:
        print(f"Error opening SSE stream: {str(e)}")
        return
    last_activity = time.time()
    for line in sse_response.iter_lines(chunk_size=1):
        if time.time() - last_activity > event_timeout:
            print(f"No activity for {event_timeout} seconds, exiting")
            break
        if line:
            last_activity = time.time()
        if not line:
            continue
        try:
            text = line.decode("utf-8")
            if text.startswith("event:"):
                event_name = text[6:].strip()
                print(f"Event name: {event_name}")
            elif text.startswith("data:"):
                data = text[5:].strip()
                print(f"Data: {data[:30]}...")
            elif text.startswith(":"):
                print("Heartbeat")
            else:
                print(f"Unknown SSE line format: {text}")
        except UnicodeDecodeError:
            print(f"Binary data received (couldn't decode as UTF-8): {line}")
    sse_response.close()
    print("SSE stream closed")

if __name__ == "__main__":
    arg_url = sys.argv[1] if len(sys.argv) > 1 else None
    test_sse_stream_read(arg_url) 