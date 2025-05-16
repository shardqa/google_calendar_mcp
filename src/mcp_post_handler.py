from .mcp_post_sse_handler import handle_post_sse
from .mcp_post_other_handler import handle_post_other

def handle_post(handler, request, response):
    if handler.path == '/sse':
        handle_post_sse(handler, request, response)
    else:
        handle_post_other(handler, request, response) 