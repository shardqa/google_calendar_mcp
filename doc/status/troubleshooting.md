# Resolução de Problemas

Este guia organiza as soluções para os problemas mais comuns encontrados no
projeto, divididas por categoria para facilitar a consulta.

## Guias Específicos

### [Problemas de Instalação e Ambiente](troubleshooting/installation_issues.md)

- Configuração inicial do projeto
- Problemas com Google APIs
- Configuração de ambiente Python
- Credenciais e autenticação

### [Problemas do Servidor MCP](troubleshooting/mcp_server_issues.md)

- Servidor não carrega código atualizado
- Ferramentas não respondem
- Problemas de conectividade
- Configuração de clientes (Cursor, Gemini CLI)

### [Problemas de Testes](troubleshooting/testing_issues.md)

- Testes lentos ou que falham
- Problemas de cobertura de código
- Issues específicos de CI/CD
- Debugging de subprocess e mocks

## Problemas Específicos

### Calendários ICS Externos

**Problema**: ICS não retorna eventos, LLM não consegue ver agenda

**Sintomas**:

- Comando retorna lista vazia mesmo com eventos
- Erros de rede não são reportados adequadamente  
- Calendários malformados quebram silenciosamente

**Soluções**:

- **Tratamento de erro gracioso**: Erros de rede agora retornam mensagens informativas
- **Debug automático**: Use `debug=True` para ver detalhes de processamento
- **Feedback melhorado**: Sistema explica quando eventos foram filtrados por data
- **Validação de formato**: Calendários malformados retornam mensagens úteis

**Comandos para diagnóstico**:

```bash
# Teste básico com debug
python -m src.commands.mcp_cli list-events --ics-url="http://example.com/cal.ics" --debug

# Teste de conectividade
curl -I http://example.com/calendar.ics

# Verificar formato ICS
python -c "import requests; print(requests.get('URL').text[:500])"
```

## Dicas Gerais

### Diagnóstico Rápido

Para problemas não cobertos nos guias específicos, tente estes passos:

1. **Verifique o ambiente**: `python --version` e confirme que está no venv correto
2. **Teste básico**: `python -m src.commands.mcp_cli --help`
3. **Logs do servidor**: Verifique a saída do console ao executar `make mcp-start`
4. **Testes unitários**: Execute `make test` para verificar se algo quebrou

### Obtendo Ajuda

Se nenhum dos guias resolver seu problema:

1. Verifique se há issues similares no repositório
2. Colete informações do sistema (OS, Python version, error logs)
3. Abra uma issue detalhada no GitHub

---
Para instruções de uso, veja [Uso](guides/usage.md).
Para melhorias planejadas, veja [Desenvolvimento Futuro](future.md).
Voltar para o [Sumário](README.md).
