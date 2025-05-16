import requests
import socket
import sys
import time

def check_server_connectivity(host="localhost", port=3001):
    """
    Test basic server connectivity without SSE features.
    This just checks if we can make HTTP requests to the server.
    """
    # First, check if the port is open at all
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((host, port))
        if result == 0:
            print(f"✅ Socket connection to {host}:{port} successful")
        else:
            print(f"❌ Could not connect to socket {host}:{port}")
            print("Is the server running? Check with: ./run_mcp.sh")
            return False
        sock.close()
    except Exception as e:
        print(f"❌ Socket error: {str(e)}")
        return False
    
    # Now try HTTP connection
    base_url = f"http://{host}:{port}"
    try:
        print(f"Testing HTTP connectivity to {base_url}...")
        response = requests.get(base_url, timeout=5)
        print(f"✅ HTTP connection successful: {response.status_code}")
        if response.status_code == 200:
            print("Response content:")
            print(response.text[:500])  # Print first 500 chars
    except Exception as e:
        print(f"❌ HTTP connection failed: {str(e)}")
        return False
    
    # Test with a simple POST to the SSE endpoint
    sse_url = f"{base_url}/sse"
    try:
        print(f"\nTesting POST to SSE endpoint {sse_url}...")
        data = {
            "method": "initialize",
            "params": {"clientInfo": {"name": "basic-test", "version": "1.0.0"}},
            "jsonrpc": "2.0",
            "id": 123
        }
        response = requests.post(
            sse_url, 
            json=data, 
            timeout=5,
            headers={'Content-Type': 'application/json'}
        )
        print(f"✅ POST to SSE endpoint successful: {response.status_code}")
        if response.status_code == 200:
            print("Response content:")
            print(response.text)
        return True
    except Exception as e:
        print(f"❌ POST to SSE endpoint failed: {str(e)}")
        return False

if __name__ == "__main__":
    # Allow specifying host and port from command line
    host = sys.argv[1] if len(sys.argv) > 1 else "localhost"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 3001
    
    print(f"Testing server at {host}:{port}")
    if check_server_connectivity(host, port):
        print("\n✅ Server is accessible and responding to requests")
    else:
        print("\n❌ Server connectivity issues detected")
        print("Possible solutions:")
        print("1. Make sure the server is running: ./run_mcp.sh")
        print("2. Check if the port is correct (default is 3001)")
        print("3. Try running the server with: python -m src.mcp_cli --port 3001")
        print("4. Check firewall settings (should not be an issue for localhost)")
        print("5. Try using 0.0.0.0 instead of localhost: python -m src.mcp_cli --host 0.0.0.0 --port 3001") 