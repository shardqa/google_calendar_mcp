import src.mcp.mcp_post_sse_handler as nested
from src.mcp_schema import get_mcp_schema

calendar_ops = nested.calendar_ops
auth = nested.auth

def handle_post_sse(handler, request, response):
    nested.get_mcp_schema = get_mcp_schema
    return nested.handle_post_sse(handler, request, response) 