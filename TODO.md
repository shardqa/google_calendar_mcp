# TODO - Atividades Ativas

## Development Tasks

### High Priority

- [ ] **URGENT**: Fix failing test `tests/unit/cli/test_mcp_cli.py::test_setup_mcp_config_handles_corrupted_file`
- [ ] **URGENT**: Fix MCP credentials.json path issue - MCP not finding credentials when running from different directories, likely using relative path instead of absolute path

### Medium Priority

- [ ] Maintain comprehensive test coverage during refactors

## Future Enhancements

- [ ] Build a lightweight web interface for unified calendar and task management
- [ ] Profile and optimize performance for large datasets

## Quality Metrics (Current)

### Test Coverage by Component

- **Core modules**: 100%
- **CLI handlers**: 90%+
- **MCP components**: 95%+
- **Utility scripts**: 95%+
- **Overall project**: 100% 🎯

### Test Quality Standards

- **231+ automated tests** with zero failures
- **Comprehensive edge case coverage** including network failures, timeouts, invalid data, Tasks error scenarios
- **Isolated unit tests** using strategic mocking for external dependencies
- **Performance optimized** test suite execution (~4 s)
- **TDD methodology** mantida durante o desenvolvimento

Para informações de arquitetura e visão geral, consulte:
[Architecture](doc/guides/architecture.md) • [Overview](doc/guides/overview.md)

- [ ] Persist external ICS calendar URLs with aliases to avoid re-passing the full URL

## Security

- [ ] Debug Cursor MCP client certificate compatibility com porta 8443 (atualmente via ZeroTier)
- [ ] Enable Nginx rate-limiting and fail2ban for brute-force protection
- [ ] Ship access/error logs to local file (debug-level) with logrotate policy
- [ ] Run dependency vulnerability scan (pip-audit) as CI step
- [ ] Document all steps in doc/guides/security_plan.md and link from README
