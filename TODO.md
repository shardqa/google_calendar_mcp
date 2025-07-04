# TODO

- [ ] Maintain comprehensive test coverage during refactors
- [ ] Build a lightweight web interface for unified calendar and task management
- [ ] Profile and optimize performance for large datasets
- [ ] Persist external ICS calendar URLs with aliases to avoid re-passing the full URL
- [ ] Ajustar retorno do list_events dos ICS para retornar compromissos detalhados e não apenas contagem
- [ ] Implementar adição de eventos em batch via arquivo ICS (importação em massa)
- [ ] Debug Cursor MCP client certificate compatibility com porta 8443 (atualmente via ZeroTier)
- [ ] Enable Nginx rate-limiting and fail2ban for brute-force protection
- [ ] Ship access/error logs to local file (debug-level) com logrotate policy
- [ ] Run dependency vulnerability scan (pip-audit) as CI step
- [ ] Document all steps in doc/guides/security_plan.md and link from README
