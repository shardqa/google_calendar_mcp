# Problemas do Servidor MCP

## Problemas de Execução

### Servidor MCP Não Carrega Código Atualizado

**Problema**: Alterações no código não são refletidas no servidor em
execução.

**Causas**: Cache Python, processo não reiniciado, porta ocupada.

**Soluções**:

```bash
# Limpeza de cache
find . -name "*.pyc" -delete && \
  find . -type d -name "__pycache__" -exec rm -rf {} +

# Reiniciar servidor
pkill -f "mcp_cli" && make mcp-start

# Liberar porta
sudo fuser -k 3001/tcp
```

### Servidor MCP Não Responde

**Problema**: Servidor parece estar rodando mas não responde adequadamente.

**Sintomas**:

- Erro "no result from tool"
- Timeout nas chamadas MCP
- Ferramentas funcionam localmente mas não via MCP

**Diagnóstico**:

```bash
# Verificar se servidor está ativo
ps aux | grep mcp_cli

# Testar conectividade
curl http://localhost:3001/sse

# Comparar com CLI local
python -m src.commands.mcp_cli list
```

**Soluções**:

```bash
# Reiniciar completamente
make mcp-restart

# Verificar logs do servidor por mensagens de erro
# Confirmar que não há conflitos de versão de código
```

## Problemas de Ferramentas

### "Tool not found"

**Problema**: Servidor retorna erro "Tool not found" para ferramentas
válidas.

**Causa**: Handlers SSE e Other precisam implementar as mesmas ferramentas.

**Solução**: Verificar se ambos `mcp_post_sse_handler.py` e
`mcp_post_other_handler.py` têm as ferramentas implementadas.

### Ferramentas MCP Não Retornam Resultados

**Problema**: Ferramentas executam no servidor mas não retornam resultados
para o cliente.

**Sintomas**:

- `list_events` funciona normalmente
- `echo` e `add_event` executam mas não retornam resposta
- Cliente recebe "no result from tool"

**Causa**: Inconsistência no formato de resposta. O cliente espera sempre:

```json
{
  "result": {
    "content": [{"type": "text", "text": "conteúdo da resposta"}]
  }
}
```

**Prevenção**: Sempre usar o formato `{"content": [{"type": "text",
"text": "..."}]}` para todas as respostas MCP.

### Gemini CLI Não Encontra Servidor

**Problema**: `gemini mcp list` não mostra o servidor `google_calendar`.

**Soluções**:

1. Verifique se o caminho em `cwd` no `~/.gemini/settings.json` é
   **absoluto** e correto
2. Confirme que `PYTHONPATH` está definido corretamente na configuração
3. Teste manualmente: `python -m src.mcp.mcp_stdio_server`

---
Voltar para [Resolução de Problemas](../troubleshooting.md).
