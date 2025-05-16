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

def test_cancel_request(url=None, timeout=10):
    """
    Test the cancellation functionality of the MCP server.
    
    This script attempts to:
    1. Initialize a connection
    2. Send a cancel request
    3. Verify the response
    
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
    
    # Step 2: Send a cancel request
    cancel_data = {
        "method": "mcp/cancel",
        "params": {},
        "jsonrpc": "2.0",
        "id": 1
    }
    
    print(f"\nSending cancel request to {url}")
    try:
        # Create a new session for the cancel request
        cancel_session = requests.Session()
        cancel_session.keep_alive = False
        
        headers = {
            'Content-Type': 'application/json',
            'Connection': 'close'
        }
        
        response = cancel_session.post(
            url, 
            json=cancel_data, 
            timeout=timeout,
            headers=headers
        )
        
        print(f"Cancel request status: {response.status_code}")
        if response.status_code != 200:
            print(f"Error: Cancel request failed with status code {response.status_code}")
            print(response.text)
            return
        
        print(f"Cancel response: {response.json()}")
        
        # Verify the response format
        result = response.json()
        if "result" in result and "cancelled" in result["result"] and result["result"]["cancelled"] == True:
            print("\n✅ Success: Server correctly responded to cancellation request")
        else:
            print("\n❌ Error: Server did not respond with proper cancellation format")
            
    except requests.exceptions.Timeout:
        print(f"Error: Cancel request timed out after {timeout} seconds")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to server for cancel request")
    except Exception as e:
        print(f"Error during cancel request: {str(e)}")

if __name__ == "__main__":
    # Allow specifying URL from command line
    url = sys.argv[1] if len(sys.argv) > 1 else None
    test_cancel_request(url) 