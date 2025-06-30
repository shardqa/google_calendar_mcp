import time
from src.mcp import mcp_server
from src.mcp.auth_middleware import RobustAuthMiddleware


def test_mcp_server_print(capsys):
    mcp_server.run_server("h", 1)
    mcp_server.main()
    assert "noop" in capsys.readouterr().out


def test_auth_stats():
    am = RobustAuthMiddleware()
    am.allowed_ips = {"5.5.5.5", "1.1.0.0/16"}
    assert am.check_ip_whitelist("1.1.2.3")
    assert am.check_ip_whitelist("5.5.5.5")
    assert not am.check_ip_whitelist("9.9.9.9")
    am.rate_limits = {"a": True}
    am.failed_attempts = {"b": [time.time() - 5 for _ in range(11)]}
    s = am.get_auth_stats()
    assert s["active_rate_limits"] == 1 and s["blocked_ips"] == 1 