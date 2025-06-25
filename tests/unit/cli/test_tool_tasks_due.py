from src.mcp.tools import tool_tasks as tt

def test_build_confirm_includes_due():
    task = {"id": "123", "title": "Do something", "due": "2025-01-01T10:00:00Z"}
    res = tt._build_confirm(task)
    txt = res["content"][0]["text"]
    assert "📅 Due:" in txt 