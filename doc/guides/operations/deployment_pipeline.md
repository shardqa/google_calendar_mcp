# Pipeline de Deploy Automatizado

## GitHub Actions

### Triggers

- Push na branch `main`
- Merge de Pull Request
- Dispatch manual

### Etapas

1. **Test Execution** – executa todos os testes  
2. **Coverage Check** – garante >99 % de cobertura  
3. **Build Validation** – checagem de integridade  
4. **Deployment** – envio automático para o servidor remoto

## Configuração do Servidor Remoto

| Parâmetro | Valor |
| --------- | ----------------------------- |
| Service   | `google-calendar-mcp.service` |
| Porta     | `3001`                        |
| Auto-restart | Habilitado                 |
| Logs      | `journalctl`                  |

A máquina é acessada preferencialmente pelo endereço ZeroTier `10.243.215.33`
utilizando o protocolo SSE autenticado por token.

---

Veja também: [Security Plan](../security_plan.md) · [Architecture](../architecture.md)
