# TODO - Atividades Ativas

## Development Tasks

### High Priority
- [x] Modificar seu servidor MCP para suportar stdio além de SSE ✅

### Medium Priority

- [ ] Refactor any directory exceeding ten items into logical sub-folders
  and adjust imports
- [ ] Maintain comprehensive test coverage during refactors

## Future Enhancements

- [ ] Build a lightweight web interface for unified calendar and task management
- [ ] Profile and optimize performance for large datasets

## Quality Metrics (Current)

### Test Coverage by Component

- **Core modules**: 100% (auth, calendar_ops, tasks_ops)
- **CLI handlers**: 100% (main, mcp_cli, tasks_cli)
- **MCP components**: 100% (handlers, server, schemas)
- **Utility scripts**: 94-96% (connectivity, initialization,
  streaming)
- **Overall project**: 100% 🏆 (246 tests passing) ✅

### Test Quality Standards

- **246+ automated tests** with zero failures
- **Comprehensive edge case coverage** including network failures,
  timeouts, invalid data, Tasks error scenarios
- **Isolated unit tests** using strategic mocking for external
  dependencies
- **Performance optimized** test suite execution (~2.8s)
- **TDD methodology** maintained throughout development

For background information, see the project [Architecture](doc/guides/architecture.md)
and [Overview](doc/guides/overview.md) documents.

- [ ] Persist external ICS calendar URLs with aliases to avoid re-passing the full URL

## Security

- [x] Establish internal certificate authority (CA) and issue server and client certificates ✅
- [x] Configure Nginx reverse-proxy front-end with HTTPS (self-signed) + mutual TLS enforcement ✅
- [ ] Update MCP client to call server over HTTPS with client certificate authentication
- [x] Restrict firewall: expose only 443 to ZeroTier interface and close 3001 externally ✅
- [ ] Enable Nginx rate-limiting and fail2ban for brute-force protection
- [ ] Ship access/error logs to local file (debug-level) with logrotate policy
- [ ] Run dependency vulnerability scan (pip-audit) as CI step
- [ ] Document all steps in doc/guides/security_plan.md and link from README
