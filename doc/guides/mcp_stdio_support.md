# Suporte a MCP stdio

## Visão Geral

O servidor MCP agora suporta comunicação via **stdio** (standard input/output) além do modo SSE (Server-Sent Events) existente. Isso permite integração com uma gama maior de clientes MCP que preferem comunicação direta via stdin/stdout.

## Como Usar

### Modo stdio

Para executar o servidor em modo stdio:

```bash
python src/commands/mcp_cli.py --stdio
```

### Modo SSE (padrão)

Para executar o servidor em modo SSE (comportamento original):

```bash
python src/commands/mcp_cli.py --host localhost --port 3000
```

## Protocolo de Comunicação

### Formato JSON-RPC

O servidor stdio segue o padrão JSON-RPC 2.0 para comunicação:

```json
{
  "jsonrpc": "2.0",
  "method": "initialize",
  "params": {},
  "id": 1
}
```

### Métodos Suportados

#### 1. `initialize`
Inicializa a conexão e retorna capacidades do servidor:

```json
{
  "jsonrpc": "2.0",
  "method": "initialize",
  "params": {},
  "id": 1
}
```

**Resposta:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "serverInfo": {
      "name": "google_calendar",
      "version": "1.0.0"
    },
    "capabilities": {
      "tools": { ... }
    },
    "protocolVersion": "2025-03-26"
  }
}
```

#### 2. `tools/list`
Lista todas as ferramentas disponíveis:

```json
{
  "jsonrpc": "2.0",
  "method": "tools/list",
  "params": {},
  "id": 2
}
```

#### 3. `tools/call`
Executa uma ferramenta específica:

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "echo",
    "arguments": {
      "message": "Hello World!"
    }
  },
  "id": 3
}
```

## Ferramentas Disponíveis

O servidor stdio expõe as mesmas ferramentas que o modo SSE:

### Google Calendar
- `echo` - Teste de conectividade
- `list_events` - Listar eventos do calendário
- `add_event` - Adicionar novo evento
- `remove_event` - Remover evento existente
- `list_calendars` - Listar calendários disponíveis

### Google Tasks
- `list_tasks` - Listar tarefas
- `add_task` - Adicionar nova tarefa
- `remove_task` - Remover tarefa existente

### Funcionalidades Avançadas
- `add_recurring_task` - Adicionar eventos recorrentes
- `schedule_tasks` - Agendamento inteligente de tarefas
- `register_ics_calendar` - Registrar calendário ICS externo
- `list_ics_calendars` - Listar calendários ICS registrados

## Exemplo de Uso Prático

### Testando com curl e pipes

```bash
# Iniciar servidor
python src/commands/mcp_cli.py --stdio &

# Enviar comando initialize
echo '{"jsonrpc": "2.0", "method": "initialize", "params": {}, "id": 1}' | \
  python src/commands/mcp_cli.py --stdio

# Listar ferramentas
echo '{"jsonrpc": "2.0", "method": "tools/list", "params": {}, "id": 2}' | \
  python src/commands/mcp_cli.py --stdio

# Testar echo
echo '{"jsonrpc": "2.0", "method": "tools/call", "params": {"name": "echo", "arguments": {"message": "Teste!"}}, "id": 3}' | \
  python src/commands/mcp_cli.py --stdio
```

### Script de Teste Automatizado

Execute o script de teste incluído:

```bash
python test_stdio.py
```

Este script executa uma bateria de testes automatizados para validar:
- Inicialização do servidor
- Listagem de ferramentas
- Execução de comandos
- Tratamento de erros

## Arquitetura Técnica

### Classe `MCPStdioServer`

A implementação do stdio está em `src/mcp/mcp_stdio_server.py`:

```python
class MCPStdioServer:
    def __init__(self):
        self.running = False
        self.capabilities = None
        self._setup_capabilities()
    
    def start(self):
        # Envia mensagem de hello inicial
        # Inicia loop de leitura do stdin
        
    def _read_stdin(self):
        # Processa requisições JSON-RPC linha por linha
        
    def _handle_request(self, request):
        # Roteia requisições para handlers apropriados
```

### Integração com Handlers Existentes

O servidor stdio reutiliza a lógica de negócio existente através do `handle_post_other`:

```python
def _handle_tools_call(self, request):
    # Cria mock handler para capturar resposta
    mock_handler = MockHandler()
    
    # Delega para handler existente
    handle_post_other(mock_handler, request, response)
    
    # Retorna resposta formatada
    return mock_handler.response_data
```

## Tratamento de Erros

### Códigos de Erro JSON-RPC

- `-32700`: Parse error (JSON inválido)
- `-32601`: Method not found (método não encontrado)
- `-32603`: Internal error (erro interno)

### Exemplo de Resposta de Erro

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32601,
    "message": "Method not found: invalid/method"
  }
}
```

## Testes

### Testes Unitários

Os testes estão em `tests/mcp/mcp_stdio_server/test_mcp_stdio_server.py`:

```bash
# Executar testes específicos do stdio
python -m pytest tests/mcp/mcp_stdio_server/ -v

# Executar todos os testes
make test
```

### Cobertura de Testes

- ✅ Inicialização do servidor
- ✅ Handlers para todos os métodos JSON-RPC
- ✅ Tratamento de erros e JSON inválido
- ✅ Integração com handlers existentes
- ✅ Mock handlers para tools/call
- ✅ Ciclo de vida do servidor (start/stop)

## Benefícios

### Compatibilidade Expandida

- **Suporte a mais clientes MCP**: Muitos clientes preferem stdio
- **Integração via pipes**: Permite uso em scripts shell
- **Modo batch**: Processamento de múltiplos comandos
- **Debug simplificado**: Entrada/saída em texto plano

### Reutilização de Código

- **Zero duplicação**: Reutiliza toda lógica de negócio existente
- **Manutenção centralizada**: Handlers compartilhados
- **Teste consistente**: Mesmas ferramentas, mesmo comportamento

## Comparação com SSE

| Aspecto | stdio | SSE |
|---------|-------|-----|
| **Protocolo** | JSON-RPC via stdin/stdout | HTTP + Server-Sent Events |
| **Clientes** | Qualquer processo | Browsers, HTTP clients |
| **Conectividade** | Processo a processo | Rede (localhost/remoto) |
| **Debug** | Simples (texto plano) | Requer ferramentas HTTP |
| **Performance** | Excelente (direto) | Boa (overhead HTTP) |
| **Uso** | Scripts, automação | Editores, UIs web |

## Próximos Passos

1. **Documentar configuração de clientes MCP** para usar modo stdio
2. **Criar exemplos de integração** com editores populares
3. **Otimizar performance** para comunicação em lote
4. **Adicionar logging estruturado** para debugging

---

Para configuração SSE, veja [Configuração MCP](mcp_configuration.md).  
Para arquitetura geral, veja [Arquitetura](architecture.md).  
Para uso básico, veja [Uso](usage.md).  
Voltar para o [Sumário](README.md).
