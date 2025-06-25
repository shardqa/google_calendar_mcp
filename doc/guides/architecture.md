# Arquitetura do Projeto

## Estrutura de Diretórios

```text
google_calendar_mcp/
├── config/               # Configurações do projeto
├── doc/                  # Documentação completa
│   ├── troubleshooting/  # Diagnósticos e soluções
│   ├── architecture.md
│   ├── intelligent_scheduling.md
│   └── tasks_integration.md
├── src/                  # Código-fonte modular
│   ├── commands/         # Interfaces de linha de comando
│   │   ├── cli.py        # CLI principal do calendário
│   │   ├── main.py       # Coordenação entre CLIs
│   │   ├── mcp_cli.py    # CLI do servidor MCP
│   │   └── tasks_cli.py  # CLI para Google Tasks
│   ├── core/             # Lógica de negócio
│   │   ├── auth.py       # Autenticação unificada
│   │   ├── calendar_ops.py # Operações de calendário
│   │   ├── cancel_utils.py # Utilitários de cancelamento
│   │   ├── ics_ops.py    # Operações de calendários ICS externos
│   │   ├── ics_registry.py # Registry de aliases para calendários ICS
│   │   ├── scheduling_engine.py # Motor de agendamento inteligente
│   │   ├── tasks_auth.py   # Autenticação Google Tasks
│   │   └── tasks_ops.py    # Operações de tarefas
│   ├── mcp/              # Protocolo MCP
│   │   ├── mcp_handler.py     # Handler principal HTTP
│   │   ├── mcp_get_handler.py # Endpoints GET
│   │   ├── mcp_post_*.py      # Handlers POST especializados
│   │   ├── mcp_schema.py      # Schema e definições
│   │   └── mcp_server.py      # Servidor HTTP threading
│   └── main.py           # Ponto de entrada principal
├── tests/                # Cobertura de testes (100%)
│   ├── auth/             # Testes de autenticação
│   ├── calendar_ops/     # Testes de operações
│   ├── cli/              # Testes de interfaces CLI
│   ├── core/             # Testes de lógica central
│   ├── integration/      # Testes de integração
│   ├── mcp_*/            # Testes do protocolo MCP
│   ├── scheduling/       # Testes do motor de agendamento
│   └── tasks/            # Testes Google Tasks
├── pytest.ini           # Configuração de testes
├── requirements.txt      # Dependências do projeto
└── TODO.md              # Planejamento e roadmap
```

## Componentes Principais

### Camada de Comandos (`src/commands/`)

#### CLI Principal (`cli.py`)

- Interface de linha de comando para operações de calendário
- Menu interativo e processamento de argumentos
- Exibição formatada de eventos e resultados
- Validação de entrada e tratamento de erros

#### CLI Google Tasks (`tasks_cli.py`)

- Interface dedicada para gerenciamento de tarefas
- Comandos `list`, `add`, `remove` com parsing robusto
- Integração com autenticação unificada
- Mensagens de feedback e tratamento de exceções

#### Coordenador MCP (`mcp_cli.py`)

- Configuração automática do arquivo `.cursor/mcp.json`
- Inicialização e controle do servidor MCP
- Argumentos de linha de comando para configuração
- Gerenciamento de portas e hosts

### Camada de Negócio (`src/core/`)

#### Autenticação Unificada (`auth.py`)

- Sistema OAuth2 compartilhado entre Calendar e Tasks
- Refresh automático de tokens com retry logic
- Persistência segura de credenciais
- Scopes configuráveis por serviço

#### Operações de Calendário (`calendar_ops.py`)

- `list_events()`: Lista eventos com filtros de data e suporte a calendar_id
- `list_calendars()`: Lista todos os IDs de calendários disponíveis
- `add_event()`: Criação com validação de campos
- `remove_event()`: Remoção segura com verificação de ID
- Tratamento robusto de erros da API

#### Operações ICS Externas (`ics_ops.py`)

- `list_events()`: Parsing de calendários ICS via URL
- Suporte a múltiplos formatos de data (ISO, datetime, date-only)
- Tratamento robusto de exceções para URLs inválidas
- Cache interno para performance e rate limiting

#### Registry ICS (`ics_registry.py`)

- Sistema persistente de aliases em `config/ics_urls.json`
- Thread-safe com locks para operações concorrentes
- `register()`: Adiciona novos aliases URL
- `get()`: Recupera URL por alias
- `list_all()`: Lista todos os calendários registrados

#### Operações de Tasks (`tasks_ops.py`)

- `list_tasks()`: Listagem com suporte a múltiplas listas
- `add_task()`: Criação com título e descrição opcional
- `remove_task()`: Remoção por ID com validação
- Integração completa com Google Tasks API

#### Motor de Agendamento (`scheduling_engine.py`)

- **Análise de calendário**: Identifica slots disponíveis entre eventos
- **Proposição de horários**: Sugere blocos de tempo para tarefas pendentes
- **Configuração flexível**: Horários de trabalho e duração máxima
- **Validação inteligente**: Evita slots menores que 30 minutos
- **Suporte a períodos**: Análise diária, semanal ou mensal
- **Integração MCP**: Comando `schedule_tasks` via Server-Sent Events

#### Utilitários (`cancel_utils.py`)

- Verificação de conectividade de rede
- Timeouts configuráveis para operações
- Helpers para cancelamento de requisições
- Logging estruturado para debugging

### Camada de Protocolo (`src/mcp/`)

#### Servidor Central (`mcp_server.py`)

- Servidor HTTP multi-thread com ThreadingHTTPServer
- Binding inteligente de interfaces (0.0.0.0 para localhost)
- Configuração de socket reutilizável
- Controle de lifecycle com start/stop thread-safe

#### Handler Principal (`mcp_handler.py`)

- Roteamento de requisições HTTP para handlers especializados
- Processamento de headers e CORS
- Delegação para GET/POST handlers
- Tratamento centralizado de erros HTTP

#### Handlers Especializados

- **GET Handler** (`mcp_get_handler.py`): Endpoints de listagem e SSE
- **POST Handler** (`mcp_post_handler.py`): Roteamento de operações POST
- **POST SSE** (`mcp_post_sse_handler.py`): Server-Sent Events e tools
- **POST Other** (`mcp_post_other_handler.py`): Operações diretas

#### Schema e Definições (`mcp_schema.py`)

- Estrutura completa dos endpoints MCP
- Documentação de parâmetros e tipos de retorno
- Metadados para integração com assistentes IA
- Especificação JSON-RPC 2.0 compatível

### Protocolo de Resposta MCP

#### Formato Padronizado

Todas as ferramentas MCP implementam o mesmo formato de resposta para garantir compatibilidade:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Conteúdo formatado da resposta"
      }
    ]
  }
}
```

#### Implementação Dual

**Handlers Paralelos**: Ambos `mcp_post_sse_handler.py` e `mcp_post_other_handler.py` implementam as mesmas ferramentas:

- `echo`: Retorna mensagem com emoji de confirmação
- `list_events`: Lista eventos formatados com data/hora (Google + ICS)
- `list_calendars`: Lista IDs de calendários Google disponíveis
- `add_event`: Cria evento e retorna confirmação visual
- `remove_event`: Remove evento com status de sucesso
- `list_tasks`: Lista tarefas do Google Tasks
- `add_task`: Cria tarefa com confirmação
- `remove_task`: Remove tarefa com validação
- `add_recurring_task`: Cria eventos recorrentes
- `schedule_tasks`: Agendamento inteligente de tarefas
- `register_ics_calendar`: Registra alias para calendário ICS externo
- `list_ics_calendars`: Lista calendários ICS registrados

#### Consistência de Formatação

**Sucessos** incluem emojis e informações estruturadas:

```text
✅ Evento criado com sucesso!
📅 Reunião de Equipe
🕐 2025-06-22T14:00:00-03:00 - 2025-06-22T15:00:00-03:00
📍 Sala de Reuniões
```

**Erros** são informativos e actionable:

```text
❌ Erro ao criar evento: Missing required parameters
```

#### Benefícios Arquiteturais

- **Compatibilidade**: Funciona com Cursor IDE e outros clientes MCP
- **Consistência**: Mesma experiência em todas as ferramentas
- **Debugabilidade**: Respostas visualmente claras e estruturadas
- **Manutenibilidade**: Formato padronizado facilita testes e evolução

## Arquitetura de Qualidade

### Estratégia de Testes

- **Test-Driven Development**: Implementação red-green-refactor
- **100% de cobertura** com 230+ testes automatizados
- **Testes paralelos**: Execução rápida com pytest-xdist
- **Mocking sofisticado**: Isolamento de dependências externas
- **Edge cases abrangentes**: Cobertura de cenários de falha e extremos
- **Correção de bugs lógicos**: Análise de branch coverage para qualidade

### Padrões de Design

- **Separação de responsabilidades**: Camadas bem definidas
- **Inversão de dependências**: Injeção via parâmetros
- **Single Responsibility**: Módulos focados em uma função
- **DRY**: Reutilização entre Calendar e Tasks APIs

---
Para visão geral, veja [Visão Geral](overview.md).
Para instalação, veja [Instalação](installation.md).
Para uso, veja [Uso](usage.md).
Para resolução de problemas, veja [Resolução de Problemas](troubleshooting.md).
Para desenvolvimento futuro, veja [Desenvolvimento Futuro](future.md).
Voltar para o [Sumário](README.md).
