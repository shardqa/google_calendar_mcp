# Arquitetura do Projeto

## Estrutura de Diretórios

```
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
│   │   ├── tasks_auth.py   # Autenticação Google Tasks
│   │   └── tasks_ops.py    # Operações de tarefas
│   ├── mcp/              # Protocolo MCP
│   │   ├── mcp_handler.py     # Handler principal HTTP
│   │   ├── mcp_get_handler.py # Endpoints GET
│   │   ├── mcp_post_*.py      # Handlers POST especializados
│   │   ├── mcp_schema.py      # Schema e definições
│   │   └── mcp_server.py      # Servidor HTTP threading
│   └── main.py           # Ponto de entrada principal
├── tests/                # Cobertura de testes (96%)
│   ├── auth/             # Testes de autenticação
│   ├── calendar_ops/     # Testes de operações
│   ├── cli/              # Testes de interfaces CLI
│   ├── core/             # Testes de lógica central
│   ├── integration/      # Testes de integração
│   ├── mcp_*/            # Testes do protocolo MCP
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
- `list_events()`: Lista eventos com filtros de data
- `add_event()`: Criação com validação de campos
- `remove_event()`: Remoção segura com verificação de ID
- Tratamento robusto de erros da API

#### Operações de Tasks (`tasks_ops.py`)
- `list_tasks()`: Listagem com suporte a múltiplas listas
- `add_task()`: Criação com título e descrição opcional
- `remove_task()`: Remoção por ID com validação
- Integração completa com Google Tasks API

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

## Arquitetura de Qualidade

### Estratégia de Testes
- **Test-Driven Development**: Implementação red-green-refactor
- **96% de cobertura** com 145+ testes automatizados
- **Testes paralelos**: Execução rápida com pytest-xdist
- **Mocking sofisticado**: Isolamento de dependências externas

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
