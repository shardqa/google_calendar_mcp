#!/usr/bin/env python3
"""
MCP Stdio Server I/O operations.
Handles reading from stdin and writing responses to stdout.
"""
import json
import sys
from typing import Dict, Any


def send_response(response: Dict[str, Any]) -> None:
    """Send JSON-RPC response to stdout. Always include 'id' (string/number, never null)."""
    if "id" not in response or response["id"] is None:
        response["id"] = ""
    try:
        response_json = json.dumps(response)
        print(response_json, flush=True)
    except Exception as e:
        fallback_error = {
            "jsonrpc": "2.0",
            "error": {
                "code": -32603,
                "message": f"Internal error: {str(e)}"
            },
            "id": ""
        }
        print(json.dumps(fallback_error), flush=True)


def create_error_response(error_code: int, message: str, request_id: str = "") -> Dict[str, Any]:
    """Create a standardized error response."""
    return {
        "jsonrpc": "2.0",
        "error": {
            "code": error_code,
            "message": message
        },
        "id": request_id
    }


def read_stdin_loop(server) -> None:
    """Read and process JSON-RPC requests from stdin."""
    try:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue

            try:
                request = json.loads(line)
                if "id" not in request or request["id"] is None:
                    continue
                response = server.handler.handle_request(request)
                if response:
                    send_response(response)

            except json.JSONDecodeError:
                error_response = create_error_response(-32700, "Parse error")
                send_response(error_response)
            except Exception as e:
                error_response = create_error_response(-32603, f"Internal error: {str(e)}")
                send_response(error_response)

    except KeyboardInterrupt:
        pass
    finally:
        server.running = False 