import requests
import json
import time
import sys
import socket

def check_server_status(host, port, timeout=2):
    """Check if a server is running on the given host and port"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False

def test_sse_connection(url=None, timeout=10):  # Increased timeout to 10 seconds
    """
    Test the SSE connection to the Google Calendar MCP server.
    
    This function sends a POST request to initialize the connection,
    then opens an SSE connection to receive events.
    
    Args:
        url: The SSE endpoint URL (if None, will try common ports)
        timeout: Timeout in seconds for requests
    """
    # If no URL provided, try to auto-detect
    if url is None:
        # Try common ports
        ports_to_try = [3001, 3000]
        host = "localhost"
        
        found_port = None
        for port in ports_to_try:
            if check_server_status(host, port):
                found_port = port
                print(f"Server detected on port {port}")
                break
        
        if found_port is None:
            print("No server detected on common ports. Please start the server or specify the URL.")
            return
        
        url = f"http://{host}:{found_port}/sse"
    
    print(f"Using URL: {url}")
    
    # Get the base URL for diagnostics
    base_url = url.rsplit('/', 1)[0]
    
    # Test connectivity to the base URL first
    try:
        print(f"Testing basic connectivity to {base_url}...")
        response = requests.get(base_url, timeout=timeout)
        print(f"Base URL connection successful: {response.status_code}")
    except Exception as e:
        print(f"Warning: Could not connect to base URL: {str(e)}")
        print("Will try the SSE endpoint directly anyway")
    
    # Step 1: Initialize with POST request
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
        # Set longer timeouts and disable keep-alive to avoid issues
        session = requests.Session()
        session.keep_alive = False
        
        # Set explicit headers
        headers = {
            'Content-Type': 'application/json',
            'Connection': 'close'
        }
        
        response = session.post(
            url, 
            json=init_data, 
            timeout=timeout,
            headers=headers
        )
        
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
    
    # Give the server a moment to process
    time.sleep(1)
    
    # Step 2: Open SSE connection
    print(f"Opening SSE connection to {url}")
    
    headers = {
        "Accept": "text/event-stream",
        "Cache-Control": "no-cache"
    }
    
    try:
        # Create a new session for the GET request
        get_session = requests.Session()
        sse_response = get_session.get(url, headers=headers, stream=True, timeout=timeout)
        
        print(f"SSE connection status: {sse_response.status_code}")
        if sse_response.status_code != 200:
            print(f"Error: SSE connection failed with status code {sse_response.status_code}")
            print(sse_response.text)
            return
        
        print("SSE connection established successfully")
    except requests.exceptions.Timeout:
        print(f"Error: SSE connection timed out after {timeout} seconds")
        return
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to server for SSE. Is the server running?")
        return
    except Exception as e:
        print(f"Error establishing SSE connection: {str(e)}")
        return
    
    # Step 3: Read events from the SSE stream with timeout
    print("Waiting for events...")
    try:
        event_data = ""
        event_name = None
        last_activity = time.time()
        timeout_duration = 20  # Increased timeout to 20 seconds
        
        for line in sse_response.iter_lines(chunk_size=1):
            # Check for timeout
            current_time = time.time()
            if current_time - last_activity > timeout_duration:
                print(f"No activity for {timeout_duration} seconds, exiting")
                break
            
            # Reset activity timer on any data
            if line:
                last_activity = current_time
            
            if not line:
                # Empty line indicates the end of an event
                if event_data:
                    print(f"Received event: {event_name}")
                    try:
                        parsed_data = json.loads(event_data)
                        print(f"Event data: {json.dumps(parsed_data, indent=2)}")
                    except json.JSONDecodeError:
                        print(f"Raw event data: {event_data}")
                    
                    event_data = ""
                    event_name = None
                continue
            
            # Decode the line
            try:
                line = line.decode('utf-8')
                print(f"Raw line: {line}")
                
                if line.startswith("event:"):
                    event_name = line[6:].strip()
                    print(f"Event name: {event_name}")
                elif line.startswith("data:"):
                    event_data = line[5:].strip()
                    print(f"Got data: {event_data[:30]}...")
                elif line.startswith(":"):
                    # This is a comment/heartbeat
                    print("Received heartbeat")
                else:
                    print(f"Unknown SSE line format: {line}")
            except UnicodeDecodeError:
                print(f"Binary data received (couldn't decode as UTF-8): {line}")
    
    except KeyboardInterrupt:
        print("Test terminated by user")
    except requests.exceptions.ChunkedEncodingError:
        print("Error: The server closed the connection unexpectedly")
    except Exception as e:
        print(f"Error during SSE connection: {str(e)}")
    finally:
        print("Closing SSE connection")
        sse_response.close()
        print("Test completed")

if __name__ == "__main__":
    # Allow specifying URL from command line
    url = sys.argv[1] if len(sys.argv) > 1 else None
    test_sse_connection(url) 