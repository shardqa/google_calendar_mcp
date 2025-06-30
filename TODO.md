# TODO - Atividades Ativas

## Development Tasks

### High Priority

- [x] Analisar e ajustar google_calendar_mcp para usar uvx ao invés de python direto na configuração MCP ✅
- [ ] Restore test coverage to 100% after large file refactoring
- [x] Remover código HTTP/SSE server - manter apenas stdio mode ✅
- [x] Remover src/mcp/mcp_server.py e dependências HTTP ✅ (stub criado)
- [x] Remover partes não-stdio do src/commands/mcp_cli.py ✅
- [x] Limpar handlers HTTP: mcp_handler.py, mcp_get_handler.py, mcp_post_*.py ✅
- [x] Remover testes relacionados a HTTP/SSE endpoints ✅
- [ ] Limpar método python direto (manter apenas uvx)
  - [ ] Remover suporte a configuração python3 direto
  - [ ] Atualizar scripts que ainda usam python direto
  - [ ] Simplificar testes de configuração MCP

### Medium Priority

- [ ] Refactor any directory exceeding ten items into logical sub-folders
  and adjust imports
- [ ] Maintain comprehensive test coverage during refactors

## Future Enhancements

- [ ] Build a lightweight web interface for unified calendar and task management
- [ ] Profile and optimize performance for large datasets

## Quality Metrics (Current)

### Test Coverage by Component

- **Core modules**: ~95-100% (most calendar functions, auth, tasks_ops)
- **CLI handlers**: 80% (mcp_cli coverage gaps)
- **MCP components**: 25-98% (stdio server needs attention)
- **Utility scripts**: 94-96% (connectivity, initialization,
  streaming)
- **Overall project**: 90% 🎯 (279 tests passing) ⚠️ (down from 100% due to refactoring)

### Test Quality Standards

- **279+ automated tests** with zero failures
- **Comprehensive edge case coverage** including network failures,
  timeouts, invalid data, Tasks error scenarios
- **Isolated unit tests** using strategic mocking for external
  dependencies
- **Performance optimized** test suite execution (~4.5s)
- **TDD methodology** maintained throughout development

For background information, see the project [Architecture](doc/guides/architecture.md)
and [Overview](doc/guides/overview.md) documents.

- [ ] Persist external ICS calendar URLs with aliases to avoid re-passing the full URL

## Security

- [x] Establish internal certificate authority (CA) and issue server and client certificates ✅
- [x] Configure Nginx reverse-proxy front-end with HTTPS (self-signed) + mutual TLS enforcement ✅
- [x] Update MCP client to call server over HTTPS with client certificate authentication ✅
- [x] Restrict firewall: expose only 443 to ZeroTier interface and close 3001 externally ✅
- [ ] Debug Cursor MCP client certificate compatibility with port 8443 (currently using ZeroTier direct access)
- [ ] Enable Nginx rate-limiting and fail2ban for brute-force protection
- [ ] Ship access/error logs to local file (debug-level) with logrotate policy
- [ ] Run dependency vulnerability scan (pip-audit) as CI step
- [ ] Document all steps in doc/guides/security_plan.md and link from README
