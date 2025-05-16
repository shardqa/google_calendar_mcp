import json
import time
from .mcp_schema import get_mcp_schema

connected_clients = set()

def handle_get(handler):
    print(f"GET request received at path: {handler.path}")
    if handler.path == '/sse':
        handler.send_response(200)
        handler.send_header('Content-Type', 'text/event-stream')
        handler.send_header('Cache-Control', 'no-cache')
        handler.send_header('Connection', 'keep-alive')
        handler.send_header('Access-Control-Allow-Origin', '*')
        handler.end_headers()

        schema = get_mcp_schema()
        supported_protocol_version = schema.get('protocol', '2025-03-26')
        capabilities_tools = {tool['name']: tool['inputSchema'] for tool in schema['tools']}
        hello = {'jsonrpc': '2.0', 'method': 'mcp/hello', 'params': {'serverInfo': {'name': 'google_calendar', 'version': '1.0.0'}, 'capabilities': {'tools': capabilities_tools}, 'protocolVersion': supported_protocol_version}}
        hello_json = json.dumps(hello)
        print(f"Sending hello: {hello_json}")
        handler.wfile.write(b"event: mcp/hello\n")
        handler.wfile.write(f"data: {hello_json}\n\n".encode('utf-8'))
        handler.wfile.flush()

        time.sleep(0.5)

        tools_list = {'jsonrpc': '2.0', 'method': 'tools/list', 'params': {'tools': schema['tools']}}
        tools_json = json.dumps(tools_list)
        print(f"Sending tools list (length: {len(tools_json)}): {tools_json[:250]}...")
        handler.wfile.write(b"event: tools/list\n")
        handler.wfile.write(f"data: {tools_json}\n\n".encode('utf-8'))
        handler.wfile.flush()

        client_id = id(handler)
        connected_clients.add(client_id)
        print(f"Client {client_id} connected. Total clients: {len(connected_clients)}")

        try:
            heartbeat_interval = 5
            while client_id in connected_clients:
                time.sleep(heartbeat_interval)
                handler.wfile.write(b":\n\n")
                handler.wfile.flush()
        except Exception as e:
            print(f"SSE connection error: {str(e)}")
        finally:
            if client_id in connected_clients:
                connected_clients.remove(client_id)
            print(f"Client {client_id} disconnected. Remaining clients: {len(connected_clients)}")
    elif handler.path == '/' or handler.path == '/schema':
        handler.send_response(200)
        handler.send_header('Content-Type', 'application/json')
        handler.send_header('Access-Control-Allow-Origin', '*')
        handler.send_header('Connection', 'close')
        handler.end_headers()

        schema = get_mcp_schema()
        handler.wfile.write(json.dumps(schema).encode())
    else:
        handler.send_response(404)
        handler.end_headers() 