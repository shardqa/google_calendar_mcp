from typing import Dict, Any

__all__ = ["handle"]

def handle(tool_name: str, tool_args: Dict[str, Any]):
    if tool_name != "echo":
        return None
    msg = tool_args.get("message", "No message provided")
    return {"result": {"content": [{"type": "text", "text": f"\U0001F50A Echo: {msg}"}]}} 