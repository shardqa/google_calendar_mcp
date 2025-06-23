# Operações e Deployment

Este documento cobre procedimentos operacionais, deployment e monitoramento do
Google Calendar MCP Server.

## Status Atual do Sistema

### Métricas de Qualidade

- **Test Coverage**: 99% com 182 testes automatizados
- **Tempo de Execução**: ~3.6 segundos para suite completa
- **CI/CD Pipeline**: GitHub Actions com deployment automatizado
- **Disponibilidade**: Servidor remoto via systemd service
- **Ferramentas MCP**: 7 ferramentas disponíveis (Calendar: 4, Tasks: 3)

### Arquitetura de Deployment

```text
Local Development → GitHub → CI/CD Pipeline → Remote Server
     ↓                ↓           ↓              ↓
  Port 3000        Actions    Tests Pass    Port 3001
  localhost        Tests      Deploy        ZeroTier IP
```

## Desenvolvimento Local

### Comandos Make Disponíveis

**Servidor MCP Local:**

```bash
# Iniciar servidor MCP na porta 3001 (desenvolvimento)
make mcp-local

# Iniciar servidor MCP padrão
make mcp-start

# Parar servidor MCP
make mcp-stop

# Reiniciar servidor MCP
make mcp-restart
```

**Testes e Qualidade:**

```bash
# Executar testes completos com cobertura
make test

# Executar testes rápidos (sem cobertura)
make test-fast

# Limpar arquivos temporários
make clean

# Ver todos os comandos disponíveis
make help
```

### Desenvolvimento com MCP Local

O comando `make mcp-local` é especialmente útil para desenvolvimento pois:

- Inicia o servidor na porta 3001 (não conflita com outros serviços)
- Configura automaticamente o arquivo `.cursor/mcp.json` para Cursor IDE
- Permite desenvolvimento e testes locais antes do deploy
- Inclui logs detalhados para debugging

**Fluxo de Desenvolvimento Recomendado:**

1. Fazer alterações no código
2. Executar `make test` para verificar 100% de cobertura
3. Executar `make mcp-local` para testar localmente
4. Testar via Cursor IDE com configuração local
5. Commit e push para deploy automático

## Deployment Automatizado

### GitHub Actions Pipeline

**Triggers:**

- Push para branch `main`
- Pull Request merge
- Manual dispatch

**Processo:**

1. **Test Execution**: Execute todos os 182 testes
2. **Coverage Check**: Verificar manutenção de 99% coverage
3. **Build Validation**: Verificar integridade do código
4. **Deployment**: Deploy automático para servidor remoto

### Configuração do Servidor Remoto

**Sistemd Service:**

- Nome: `google-calendar-mcp.service`
- Porta: 3001
- Auto-restart: Habilitado
- Logs: Via journalctl

**Acesso de Rede:**

- IP Externo: ***REMOVED*** (restrito)
- ZeroTier IP: 10.243.215.33 (recomendado)
- Protocolo: HTTP/MCP

## Monitoramento e Manutenção

### Verificação de Saúde

**Testes de Conectividade:**

```bash
# Verificar servidor ativo
curl http://10.243.215.33:3001/health

# Testar ferramentas MCP
python -m src.mcp_cli --port 3001 --host 10.243.215.33
```

**Logs do Sistema:**

```bash
# Status do serviço
sudo systemctl status google-calendar-mcp

# Logs em tempo real
sudo journalctl -u google-calendar-mcp -f

# Últimas 100 linhas
sudo journalctl -u google-calendar-mcp -n 100
```

### Procedimentos de Manutenção

**Restart do Serviço:**

```bash
sudo systemctl restart google-calendar-mcp
```

**Update de Código:**

```bash
# No servidor remoto
cd /path/to/google_calendar_mcp
git pull origin main
sudo systemctl restart google-calendar-mcp
```

**Limpeza de Cache:**

```bash
find . -name "*.pyc" -delete
find . -type d -name "__pycache__" -exec rm -rf {} +
```

## Resolução de Problemas Operacionais

### Servidor Não Responde

1. **Verificar Status do Serviço:**

   ```bash
   sudo systemctl status google-calendar-mcp
   ```

2. **Verificar Porta:**

   ```bash
   sudo netstat -tlnp | grep 3001
   ```

3. **Reiniciar Serviço:**

   ```bash
   sudo systemctl restart google-calendar-mcp
   ```

### Testes Falhando em CI/CD

**Problemas Comuns:**

- Paths hardcoded do Python
- Subprocess incompatível com GitHub Actions
- Timeout em testes de rede

**Diagnóstico:**

```bash
# Localmente - executar mesmos testes do CI
.venv/bin/python -m pytest --tb=short
```

### Conectividade MCP

**Configuração Correta (.cursor/mcp.json):**

```json
{
  "servers": {
    "google-calendar-mcp": {
      "command": "python",
      "args": ["-m", "src.mcp_cli", "--port", "3001", "--host", "10.243.215.33"]
    }
  }
}
```

## APIs e Dependências Externas

### Google Cloud APIs Requeridas

1. **Google Calendar API**
   - Status: Habilitada
   - Quota: Monitorar uso diário
   - Credenciais: OAuth2 (`credentials.json`)

2. **Google Tasks API**
   - Status: Habilitada (crítico para funcionalidade)
   - Primeira configuração: Pode levar alguns minutos
   - Scopes: `auth/calendar` + `auth/tasks`

### Renovação de Tokens

**Automática:**

- Refresh tokens gerenciados automaticamente
- Token storage: `token.pickle`

**Manual (se necessário):**

```bash
# Forçar nova autenticação
rm token.pickle
python -m src.cli auth
```

## Métricas e KPIs

### Performance

- **Test Suite**: <4 segundos
- **Startup Time**: <2 segundos
- **Memory Usage**: <50MB
- **Response Time**: <100ms por operação

### Confiabilidade

- **Uptime**: >99.9%
- **Test Coverage**: >99%
- **Zero Failed Tests**: Ambiente de produção
- **Auto-recovery**: Via systemd

### Capacidade

- **Concurrent Connections**: Suporte múltiplas sessões MCP
- **API Rate Limits**: Respeitados automaticamente
- **Storage**: Mínimo (apenas tokens e logs)

---
Para configuração inicial, veja [Instalação](installation.md).
Para problemas específicos, veja [Troubleshooting](troubleshooting.md).
Para configuração remota, veja [MCP Remote Setup](mcp_remote_setup.md).
Voltar para o [Sumário](README.md).
