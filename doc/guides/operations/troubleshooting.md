# Troubleshooting

## Servidor Não Responde

```bash
sudo systemctl status google-calendar-mcp
sudo netstat -tlnp | grep 3001
sudo systemctl restart google-calendar-mcp
```

## Testes Falhando em CI/CD

Problemas comuns:

- Paths hard-coded
- Timeout em testes de rede
- Subprocess incompatível com GitHub Actions

Para diagnosticar localmente:

```bash
.venv/bin/python -m pytest --tb=short
```

## Conectividade MCP

Consulte o exemplo de configuração `.cursor/mcp.json` presente no guia
[Instalação](../installation.md).

---

Links úteis: [Monitoramento](monitoring_maintenance.md) · [Overview](../overview.md)
