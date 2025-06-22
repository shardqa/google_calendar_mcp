# Google Calendar MCP

Servidor MCP (Model Context Protocol) completo para integração de Google
Calendar e
Google Tasks com assistentes de IA. Oferece interface unificada para
gerenciamento de eventos e tarefas, com suporte a execução local e remota.

## Características Principais

- **Gerenciamento de Calendário**: Listar, adicionar e remover eventos
- **Integração Google Tasks**: Operações completas de CRUD para tarefas
- **Agendamento Inteligente**: Análise automática de agenda e proposição de horários
- **Servidor MCP Remoto**: Execução como serviço via systemd
- **Alta Confiabilidade**: 100% de cobertura de testes com 230+ testes
  automatizados
- **CI/CD Automatizada**: Pipeline GitHub Actions com deployment contínuo

## Documentação

- [Visão Geral](doc/overview.md)
- [Instalação](doc/installation.md)
- [Arquitetura](doc/architecture.md)
- [Uso](doc/usage.md)
- [Configuração Remota](doc/mcp_remote_setup.md)
- [Resolução de Problemas](doc/troubleshooting.md)
- [Desenvolvimento Futuro](doc/future.md)
- [Índice Completo](doc/README.md)

## Uso como Servidor MCP

O módulo suporta execução como servidor MCP para integração com Cursor AI e
outras ferramentas compatíveis.

Para iniciar o servidor MCP local:

```bash
python -m src.mcp_cli
```

Opções disponíveis:

- `--port PORT`: Porta para executar o servidor (padrão: 3000)
- `--host HOST`: Host para o servidor (padrão: localhost)
- `--setup-only`: Apenas configurar o arquivo MCP sem iniciar o servidor

O comando irá automaticamente configurar o arquivo `.cursor/mcp.json` com as
informações do servidor.

### Ferramentas Disponíveis via MCP

**Calendário:**

- `list_events`: Listar eventos próximos
- `add_event`: Criar novos eventos com título, descrição, horário e localização
- `remove_event`: Remover eventos existentes

**Tarefas (Google Tasks):**

- `list_tasks`: Listar tarefas pendentes
- `add_task`: Criar tarefas com título, notas e prazo
- `remove_task`: Marcar tarefas como concluídas

**Agendamento Inteligente:**

- `schedule_tasks`: Analisar agenda e propor horários para tarefas
- `add_recurring_task`: Criar eventos recorrentes com frequência
  configurável

**Utilitários:**

- `echo`: Teste de conectividade e validação

## Exemplos Práticos de Uso

### Gerenciamento Básico de Eventos

**Listar eventos da semana:**

```bash
# Via MCP tool call
mcp_google_calendar_list_events max_results=10
```

**Criar reunião com detalhes completos:**

```bash
# Via MCP tool call
mcp_google_calendar_add_event 
  summary="Reunião de planejamento sprint"
  start_time="2024-03-25T14:00:00"
  end_time="2024-03-25T15:30:00"
  location="Sala de conferências A"
  description="Revisar objetivos e definir tarefas para próxima sprint"
```

### Integração com Google Tasks

**Adicionar tarefa com prazo:**

```bash
# Via MCP tool call
mcp_google_calendar_add_task
  title="Finalizar relatório mensal"
  notes="Incluir dados de Q1 e análise de performance"
  due="2024-03-28T17:00:00"
```

**Listar tarefas pendentes:**

```bash
# Via MCP tool call
mcp_google_calendar_list_tasks
```

### Agendamento Inteligente

**Analisar agenda e propor horários para tarefas:**

```bash
# Via MCP tool call
mcp_google_calendar_schedule_tasks
  time_period="week"
  work_hours_start="09:00"
  work_hours_end="18:00"
  max_task_duration=120
```

**Exemplo de output do schedule_tasks:**

```json
{
  "analysis": {
    "total_events": 8,
    "available_slots": 12,
    "pending_tasks": 5
  },
  "proposed_schedule": [
    {
      "task": "Finalizar relatório mensal",
      "suggested_time": "2024-03-26T10:00:00 - 11:30:00",
      "duration": 90,
      "rationale": "Slot livre entre reuniões, duração adequada para tarefa complexa"
    }
  ]
}
```

### Tarefas Recorrentes

**Criar lembrete de medicação:**

```bash
# Via MCP tool call
mcp_google_calendar_add_recurring_task
  summary="Tomar medicação matinal"
  frequency="daily"
  count=30
  start_time="2024-03-20T08:00:00"
  end_time="2024-03-20T08:15:00"
  description="Lembrete diário - medicação hipertensão"
```

**Reunião semanal de equipe:**

```bash
# Via MCP tool call
mcp_google_calendar_add_recurring_task
  summary="Weekly Team Sync"
  frequency="weekly"
  count=12
  start_time="2024-03-25T09:00:00"
  end_time="2024-03-25T10:00:00"
  location="Zoom: https://company.zoom.us/j/123456789"
```

### Fluxos de Trabalho Típicos

**1. Planejamento Semanal Automatizado:**

```text
1. Executar schedule_tasks para analisar a semana
2. Revisar propostas de agendamento
3. Criar eventos automáticos para tarefas prioritárias
4. Ajustar conforme necessário
```

**2. Gestão de Projetos:**

```text
1. Adicionar tarefas do projeto via add_task
2. Usar schedule_tasks para distribuir ao longo da semana
3. Criar lembretes recorrentes para check-ins
4. Monitorar progresso via list_events/list_tasks
```

**3. Integração com Assistentes AI:**

```text
- "Agende minhas tarefas para esta semana"
- "Crie um lembrete recorrente para exercícios"
- "Qual é a próxima reunião e o que preciso preparar?"
- "Reorganize minha agenda considerando a nova prioridade"
```

## Configuração Inicial

### Pré-requisitos

1. **Google Cloud Project** com as seguintes APIs habilitadas:
   - Google Calendar API
   - Google Tasks API

2. **Credenciais OAuth2** (`credentials.json`) na raiz do projeto

3. **Python 3.8+** com ambiente virtual configurado

### Execução de Testes

```bash
make test          # Suite completa com coverage
make test-fast     # Testes rápidos sem coverage
```

## Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Siga a metodologia TDD: teste falhando → implementação → refatoração
4. Mantenha cobertura de testes acima de 95%
5. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
6. Push para a branch (`git push origin feature/nova-feature`)
7. Crie um Pull Request

## Licença

Este projeto está licenciado sob a MIT License - veja o arquivo LICENSE para detalhes.
