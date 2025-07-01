# Arquitetura do Projeto

Este documento descreve a estrutura de alto nível do projeto, seus componentes principais e a organização do código-fonte. Para uma discussão detalhada sobre os *princípios* que guiam esta arquitetura, consulte as **[Boas Práticas de Arquitetura](architectural_principles.md)**.

## Estrutura de Diretórios

A estrutura de diretórios é projetada para refletir a separação de responsabilidades e facilitar a navegação.

```text
google_calendar_mcp/
├── config/               # Configurações de deploy (Nginx, systemd)
├── doc/                  # Documentação
│   ├── guides/           # Guias específicos
│   └── troubleshooting/  # Solução de problemas
├── scripts/              # Scripts de automação (segurança, testes)
├── src/                  # Código-fonte
│   ├── commands/         # CLI (`mcp_cli.py`)
│   ├── core/             # Lógica de negócio principal
│   │   ├── calendar/     # Funções modulares do Google Calendar
│   │   ├── scheduling/   # Motor de agendamento
│   │   └── ...           # Outros módulos de core
│   ├── mcp/              # Implementação do Protocolo MCP
│   │   ├── auth/         # Componentes de autenticação
│   │   ├── tools/        # Definição das ferramentas MCP
│   │   └── ...           # Handlers e servidor
│   └── main.py           # Ponto de entrada legado
├── tests/                # Testes automatizados
│   ├── unit/             # Testes unitários por módulo
│   ├── integration/      # Testes de integração E2E
│   └── mcp/              # Testes específicos do protocolo
└── ...                   # Arquivos de configuração (Makefile, etc.)
```

## Componentes Principais

### Camada de Negócio (`src/core/`)

O coração da aplicação, contendo toda a lógica de negócio desacoplada de protocolos de comunicação.

-   **Operações de Calendário (`src/core/calendar/`)**: Funções puras e modulares para cada ação no Google Calendar (`list_events`, `add_event`, etc.). Cada função é autocontida e facilmente testável.
-   **Operações de Tarefas (`src/core/tasks_ops.py`)**: Lógica para interagir com a API do Google Tasks.
-   **Motor de Agendamento (`src/core/scheduling/`)**: Componentes responsáveis pela lógica de agendamento inteligente.

### Camada MCP (`src/mcp/`)

Implementa o *Model Context Protocol*, permitindo a comunicação com assistentes de IA.

-   **Autenticação (`src/mcp/auth/`)**: Componentes modulares como `TokenVerifier` e `RateLimiter` que foram extraídos do middleware principal.
-   **Handlers de Protocolo (`mcp_post_sse_handler.py`, `stdio_handler.py`)**: Lógica específica para lidar com diferentes transportes de comunicação (HTTP SSE e STDIO).
-   **Definição de Ferramentas (`src/mcp/tools/`)**: Módulos que definem o contrato de cada ferramenta exposta pelo MCP, como `tool_calendar.py` e `tool_tasks.py`.

## Arquitetura de Qualidade e Testes

A estratégia de qualidade é um pilar do projeto, focada em garantir robustez e manutenibilidade.

-   **Estratégia de Testes**: Cobertura extensiva com mais de 279 testes, divididos em unitários, de integração e específicos para o MCP. A metodologia TDD é seguida rigorosamente.
-   **Lições Aprendidas com Refatoração**: Os desafios enfrentados durante a modularização, como a gestão de "import cascades" e a preservação de APIs públicas, estão documentados nas **[Boas Práticas de Refatoração](refactoring_best_practices.md)**.
-   **Preservação de APIs Públicas**: Durante refatorações internas, as APIs públicas expostas pelos pacotes (via `__init__.py`) são mantidas para não quebrar os consumidores.

---
Para uma visão geral do projeto, veja [Visão Geral](overview.md).
Para guias de instalação e uso, veja a [Documentação](README.md).
