# Uso

## Executando a Aplicação

Execute o programa a partir da raiz do projeto:

```bash
python -m src.main
```

Na primeira execução, você será redirecionado para o navegador para autorizar o
acesso ao seu Google Calendar.

## Executando o Servidor MCP

### Início Rápido

Para usar com Cursor, execute o servidor MCP:

```bash
# Usando Make (recomendado)
make mcp-start

# Ou usando script direto
src/scripts/run_mcp.sh

# Ou comando manual
python -m src.commands.mcp_cli --port 3001
```

### Para Gemini CLI

Para usar com Google Gemini CLI:

```bash
# Servidor stdio (automático via configuração)
python -m src.mcp.mcp_stdio_server

# Teste direto
echo '{"jsonrpc": "2.0", "method": "tools/list", "params": {}, "id": 1}' | python -m src.mcp.mcp_stdio_server
```

### Gerenciamento do Servidor

```bash
# Iniciar servidor
make mcp-start

# Parar servidor
make mcp-stop

# Reiniciar servidor
make mcp-restart

# Ver ajuda
make help
```

O servidor estará disponível em `http://localhost:3001/sse` para conexões SSE.

### Ferramentas Disponíveis

O servidor MCP oferece 15+ ferramentas:

**Google Calendar:**

- `echo` - Teste de conexão
- `list_events` - Listar eventos do calendário com informações detalhadas
  (data/hora, localização, descrição)
- `list_calendars` - Listar calendários disponíveis
- `add_event` - Adicionar novos eventos
- `edit_event` - Editar eventos existentes
- `remove_event` - Remover eventos existentes
- `add_recurring_task` - Criar tarefas recorrentes (diário, semanal, mensal)
  como lembretes de medicação

**Google Tasks:**

- `list_tasks` - Listar tarefas pendentes
- `add_task` - Adicionar novas tarefas
- `remove_task` - Remover tarefas existentes
- `complete_task` - Marcar tarefas como concluídas
- `update_task_status` - Atualizar status de tarefas

**Agendamento Inteligente:**

- `schedule_tasks` - Agendamento inteligente baseado em disponibilidade

**Calendários ICS Externos:**

- `register_ics_calendar` - Registrar calendários ICS externos
- `list_ics_calendars` - Listar calendários ICS registrados

## Uso com Diferentes Clientes

### Cursor

```bash
# Listar próximos eventos
@mcp_google_calendar_list_events max_results=5

# Adicionar evento
@mcp_google_calendar_add_event summary="Reunião importante" \
  start_time="2024-03-25T10:00:00" end_time="2024-03-25T11:00:00"

# Agendamento inteligente
@mcp_google_calendar_schedule_tasks time_period="day" \
  work_hours_start="09:00" work_hours_end="18:00"
```

### Gemini CLI

```bash
# Configuração necessária (uma vez)
export GEMINI_API_KEY="sua_chave_api"

# Uso natural
gemini "Liste meus próximos 5 eventos do calendário"
gemini "Adicione uma reunião amanhã às 15h sobre projeto MCP"
gemini "Quais tarefas tenho pendentes no Google Tasks?"
gemini "Agende minhas tarefas pendentes para esta semana"

# Exemplos específicos
gemini "Use o echo tool para testar: funcionando!"
gemini "Mostre meus calendários disponíveis"
gemini "Crie um lembrete diário para tomar remédio às 8h por 30 dias"
```

### Claude Desktop

```bash
# Comandos naturais
"List my upcoming calendar events"
"Add a meeting tomorrow at 3pm about MCP project"
"What tasks do I have pending in Google Tasks?"
"Schedule my pending tasks for this week"
"Use the echo tool to test: working!"
```

### Tarefas Recorrentes

O sistema agora suporta criação de tarefas recorrentes através do Google Calendar,
ideal para atividades repetitivas como:

- Lembretes de medicação
- Exercícios diários
- Reuniões semanais
- Check-ups mensais

**Exemplo de uso:**

```bash
# Cursor
@mcp_google_calendar_add_recurring_task \
  summary="Tomar medicação" \
  frequency="daily" \
  count=30 \
  start_time="2024-03-20T08:00:00Z" \
  end_time="2024-03-20T08:30:00Z" \
  description="Lembrete diário - medicação da manhã"

# Gemini CLI
gemini "Crie um lembrete diário para tomar remédio às 8h por 30 dias"

# Claude Desktop
"Create a daily reminder to take medication at 8am for 30 days"
```

**Frequências suportadas:**

- `daily`: Recorrência diária
- `weekly`: Recorrência semanal  
- `monthly`: Recorrência mensal

### Exibição Aprimorada de Eventos

Os eventos do calendário agora exibem informações completas:

- 📅 Data e hora de início/fim
- 📍 Localização (quando disponível)
- 📝 Descrição (quando disponível)
- Formatação visual com emojis para melhor legibilidade

## Exemplos Avançados e Cenários de Uso

### Cenário 1: Planejamento de Sprint de Desenvolvimento

**Contexto:** Equipe de desenvolvimento planeja uma sprint de 2 semanas

```bash
# 1. Listar eventos existentes para verificar conflitos
mcp_google_calendar_list_events max_results=20

# 2. Adicionar reuniões da sprint
mcp_google_calendar_add_event
  summary="Sprint Planning"
  start_time="2024-03-25T09:00:00"
  end_time="2024-03-25T11:00:00"
  location="Sala de reuniões"
  description="Planejamento da Sprint 12 - definir objetivos e distribuir tarefas"

# 3. Criar daily standups recorrentes
mcp_google_calendar_add_recurring_task
  summary="Daily Standup"
  frequency="daily"
  count=10
  start_time="2024-03-26T09:00:00"
  end_time="2024-03-26T09:15:00"
  location="Zoom: https://company.zoom.us/j/123456"

# 4. Adicionar tarefas específicas
mcp_google_calendar_add_task
  title="Implementar autenticação OAuth"
  notes="Usar Google OAuth 2.0, documentar processo"
  due="2024-03-29T17:00:00"

# 5. Usar agendamento inteligente para otimizar desenvolvimento
mcp_google_calendar_schedule_tasks
  time_period="week"
  work_hours_start="09:00"
  work_hours_end="17:00"
  max_task_duration=240
```

### Cenário 2: Gestão de Saúde Pessoal

**Contexto:** Organizar rotina de saúde com medicações e consultas

```bash
# 1. Medicação diária
mcp_google_calendar_add_recurring_task
  summary="💊 Medicação - Hipertensão"
  frequency="daily"
  count=90
  start_time="2024-03-20T08:00:00"
  end_time="2024-03-20T08:05:00"
  description="Losartana 50mg + Hidroclorotiazida 12.5mg"

# 2. Exercícios regulares
mcp_google_calendar_add_recurring_task
  summary="🏃‍♂️ Caminhada 30min"
  frequency="daily"
  count=30
  start_time="2024-03-20T18:00:00"
  end_time="2024-03-20T18:30:00"
  location="Parque da cidade"

# 3. Consultas médicas
mcp_google_calendar_add_event
  summary="🩺 Cardiologista - Dr. Silva"
  start_time="2024-03-28T14:30:00"
  end_time="2024-03-28T15:30:00"
  location="Clínica CardioLife - Sala 205"
  description="Consulta de retorno - levar exames de sangue"

# 4. Adicionar lembrete para exames
mcp_google_calendar_add_task
  title="Agendar exames de sangue"
  notes="Colesterol, glicemia, função renal"
  due="2024-03-22T12:00:00"
```

### Cenário 3: Coordenação de Projeto Multi-equipes

**Contexto:** Gerenciar projeto com múltiplas equipes e deadlines

```bash
# 1. Verificar disponibilidade das equipes
mcp_google_calendar_schedule_tasks
  time_period="month"
  work_hours_start="08:00"
  work_hours_end="18:00"
  max_task_duration=180

# 2. Reuniões de checkpoint semanais
mcp_google_calendar_add_recurring_task
  summary="📊 Checkpoint Projeto Alpha"
  frequency="weekly"
  count=8
  start_time="2024-03-22T15:00:00"
  end_time="2024-03-22T16:00:00"
  location="Hybrid: Sala 3 + Teams"
  description="Status update das 3 equipes + próximos passos"

# 3. Marcos importantes do projeto
mcp_google_calendar_add_event
  summary="🎯 Milestone: Protótipo MVP"
  start_time="2024-04-05T09:00:00"
  end_time="2024-04-05T17:00:00"
  description="Entrega do MVP para validação interna"

# 4. Tarefas críticas no backlog
mcp_google_calendar_add_task
  title="Definir arquitetura de dados"
  notes="Escolher entre PostgreSQL vs MongoDB, documentar decisão"
  due="2024-03-26T17:00:00"
```

### Cenário 4: Rotina de Estudos e Certificações

**Contexto:** Preparação para certificação técnica com cronograma estruturado

```bash
# 1. Sessões de estudo diárias
mcp_google_calendar_add_recurring_task
  summary="📚 Estudo AWS Solutions Architect"
  frequency="daily"
  count=60
  start_time="2024-03-20T19:00:00"
  end_time="2024-03-20T21:00:00"
  description="Capítulos 1-3: Fundamentals + hands-on labs"

# 2. Simulados semanais
mcp_google_calendar_add_recurring_task
  summary="✅ Simulado AWS SAA-C03"
  frequency="weekly"
  count=8
  start_time="2024-03-23T09:00:00"
  end_time="2024-03-23T11:00:00"
  description="Simulado completo + revisão de gaps"

# 3. Data da prova
mcp_google_calendar_add_event
  summary="🎓 PROVA: AWS Solutions Architect"
  start_time="2024-05-15T10:00:00"
  end_time="2024-05-15T12:30:00"
  location="Centro de Testes Pearson VUE"
  description="Chegar 30min antes. Doc: RG + CPF"

# 4. Usar IA para otimizar cronograma de estudos
mcp_google_calendar_schedule_tasks
  time_period="week"
  work_hours_start="19:00"
  work_hours_end="22:00"
  max_task_duration=120
```

### Integração com Assistentes AI - Comandos Comuns

**Perguntas típicas que o sistema pode responder:**

```bash
# Análise de agenda
"Como está minha agenda para amanhã?"
"Tenho tempo livre na quinta-feira?"
"Quais são minhas próximas 5 reuniões?"

# Gestão de tarefas
"Quais tarefas estão atrasadas?"
"Agende tempo para terminar o relatório"
"Crie um lembrete para ligar para o cliente"

# Planejamento inteligente
"Reorganize minha semana considerando a nova prioridade"
"Sugira horários para minhas tarefas pendentes"
"Quando posso encaixar uma reunião de 1 hora?"

# Análise de produtividade
"Quantas horas tenho livres esta semana?"
"Qual é o melhor horário para tarefas que exigem concentração?"
"Como distribuir 3 tarefas de 2 horas cada ao longo da semana?"
```

## Comandos CLI Disponíveis

1. **Listar eventos**: Exibe os próximos eventos do calendário.
2. **Adicionar evento**: Solicita título, descrição, data e hora para criar um evento.
3. **Remover evento**: Solicita o ID do evento para removê-lo.

---
Em caso de problemas, consulte [Resolução de Problemas](troubleshooting.md).
Para melhorias planejadas, consulte [Desenvolvimento Futuro](future.md).
Voltar para o [Sumário](README.md).
