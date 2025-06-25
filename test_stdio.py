#!/usr/bin/env python3
"""
Test script for MCP stdio server.
This script sends JSON-RPC requests to test the stdio functionality.
"""
import json
import subprocess
import sys
import time
from pathlib import Path

def test_stdio_server():
    """Test the MCP stdio server with various requests."""
    
    # Path to the CLI script
    cli_path = Path(__file__).parent / "src" / "commands" / "mcp_cli.py"
    
    # Start the server in stdio mode
    process = subprocess.Popen(
        [sys.executable, str(cli_path), "--stdio"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=0
    )
    
    def send_request(request):
        """Send a request and get response."""
        request_json = json.dumps(request)
        print(f"Sending: {request_json}")
        
        process.stdin.write(request_json + "\n")
        process.stdin.flush()
        
        # Read response
        response_line = process.stdout.readline().strip()
        print(f"Received: {response_line}")
        
        try:
            return json.loads(response_line)
        except json.JSONDecodeError as e:
            print(f"Failed to parse response: {e}")
            return None
    
    try:
        # Wait a moment for server to start
        time.sleep(1)
        
        # Test 1: Initialize
        print("\n=== Test 1: Initialize ===")
        init_request = {
            "jsonrpc": "2.0",
            "method": "initialize",
            "params": {},
            "id": 1
        }
        init_response = send_request(init_request)
        
        if init_response and "result" in init_response:
            print("✅ Initialize successful")
            print(f"Server info: {init_response['result'].get('serverInfo', {})}")
            print(f"Protocol version: {init_response['result'].get('protocolVersion', 'Unknown')}")
        else:
            print("❌ Initialize failed")
        
        # Test 2: Tools list
        print("\n=== Test 2: Tools List ===")
        tools_request = {
            "jsonrpc": "2.0",
            "method": "tools/list",
            "params": {},
            "id": 2
        }
        tools_response = send_request(tools_request)
        
        if tools_response and "result" in tools_response:
            tools = tools_response["result"].get("tools", [])
            print(f"✅ Tools list successful - {len(tools)} tools found")
            for tool in tools[:3]:  # Show first 3 tools
                print(f"  - {tool.get('name', 'Unknown')}: {tool.get('description', 'No description')}")
        else:
            print("❌ Tools list failed")
        
        # Test 3: Echo tool
        print("\n=== Test 3: Echo Tool ===")
        echo_request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": "echo",
                "arguments": {
                    "message": "Hello from stdio test!"
                }
            },
            "id": 3
        }
        echo_response = send_request(echo_request)
        
        if echo_response and "result" in echo_response:
            print("✅ Echo tool successful")
            content = echo_response["result"].get("content", [])
            if content and len(content) > 0:
                print(f"Echo response: {content[0].get('text', 'No text')}")
        else:
            print("❌ Echo tool failed")
        
        # Test 4: Invalid method
        print("\n=== Test 4: Invalid Method ===")
        invalid_request = {
            "jsonrpc": "2.0",
            "method": "invalid/method",
            "params": {},
            "id": 4
        }
        invalid_response = send_request(invalid_request)
        
        if invalid_response and "error" in invalid_response:
            print("✅ Invalid method properly rejected")
            print(f"Error: {invalid_response['error'].get('message', 'Unknown error')}")
        else:
            print("❌ Invalid method not properly handled")
        
    except Exception as e:
        print(f"Test error: {e}")
    
    finally:
        # Clean up
        try:
            process.terminate()
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
        
        print("\n=== Test Complete ===")

if __name__ == "__main__":
    test_stdio_server()
