import src.mcp.mcp_get_handler as nested
from src.mcp_schema import get_mcp_schema

time = nested.time
connected_clients = nested.connected_clients

def handle_get(handler):
    nested.get_mcp_schema = get_mcp_schema
    return nested.handle_get(handler) 