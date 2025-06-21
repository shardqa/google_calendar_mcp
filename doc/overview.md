# Visão Geral

O Google Calendar MCP é uma ferramenta completa que integra Google Calendar
e Google Tasks através do protocolo MCP (Model Context Protocol). O sistema
oferece uma interface unificada para gerenciamento de eventos e tarefas,
tanto via linha de comando quanto através de assistentes de IA.

## Funcionalidades Principais

### Gerenciamento de Calendário

- **Listar eventos**: Eventos com informações detalhadas incluindo data/hora,
  localização e descrição com formatação visual
- **Adicionar eventos**: Crie eventos com título, descrição, data, hora e localização
- **Tarefas recorrentes**: Sistema híbrido para criar eventos recorrentes
  (diário, semanal, mensal) usando Google Calendar para lembretes persistentes
- **Remover eventos**: Exclua eventos existentes pelo ID com tratamento de erros
- **Autenticação OAuth2**: Conexão segura com refresh automático de tokens

### Integração Google Tasks

- **Gerenciamento de tarefas**: Operações completas de CRUD para tarefas
- **Interface CLI**: Comandos `tasks list`, `tasks add`, `tasks remove`
- **Integração MCP**: Acesso a tarefas através do protocolo MCP
- **Autenticação unificada**: Mesmo sistema de auth para calendário e tarefas
- **Configuração da API**: Requer habilitação da Google Tasks API no
  Google Cloud Console

### Servidor MCP Remoto

- **Acesso via rede**: Suporte a configuração de servidor remoto
- **ZeroTier Integration**: Compatibilidade com redes mesh para acesso seguro
- **Systemd Service**: Execução como serviço do sistema para alta disponibilidade
- **8 Ferramentas disponíveis**: Echo, Calendar (list/add/remove events,
  add recurring tasks), Tasks (list/add/remove tasks)

### Scripts Utilitários e Diagnóstico

- **Conectividade**: Scripts para verificação de portas e conectividade HTTP
- **Inicialização SSE**: Teste de endpoints e configuração de conexões
- **Debug de streams**: Validação de comunicação em tempo real
- **Cancelamento**: Utilitários para teste de interrupção e cleanup

### Agendamento Inteligente (Planejado)

- **Organização automática**: Análise de tarefas e compromissos existentes
- **Priorização inteligente**: Algoritmo baseado em prazos e importância
- **Sugestão de blocos**: Proposta de horários otimizados para produtividade
- **Integração completa**: Sincronização entre eventos e conclusão de tarefas

## Arquitetura de Qualidade

### Cobertura de Testes Atual

- **100% de cobertura total** com 193 testes automatizados
  (725 statements, 178 branches)
- **100% de cobertura** em todos os módulos críticos (auth, CLI, operações
  principais, handlers MCP)
- **100% de cobertura de branches** em todos os handlers MCP
- **Zero testes falhando** em ambiente de produção e CI/CD

### Estratégias de Teste

- **Metodologia TDD**: Desenvolvimento orientado por testes
- **Testes unitários isolados**: Mocking estratégico de dependências externas
- **Cobertura de edge cases**: Timeouts, erros HTTP, falhas de decodificação,
  frequências inválidas
- **Testes de integração**: Validação de fluxos completos de usuário
- **Performance otimizada**: Suite completa executando em ~3.0 segundos
- **CI/CD robusta**: GitHub Actions com testes automatizados e deployment

### Estrutura Modular

- **Separação clara** entre autenticação, operações e interfaces
- **Reutilização de código** entre funcionalidades de calendário e tarefas
- **Tratamento robusto de erros** em todas as operações
- **Scripts de diagnóstico** para troubleshooting e validação
- **Documentação abrangente** com exemplos práticos

### Qualidade de Código

- **Organização por responsabilidade**: Commands, Core, MCP, Scripts
- **Limite de complexidade**: Máximo 100 linhas por arquivo, 10 itens por pasta
- **Convenções consistentes**: Nomenclatura padronizada e estrutura modular
- **Manutenibilidade**: Código autodocumentado sem comentários desnecessários

---
Para instalação, veja [Instalação](installation.md).
Para arquitetura, veja [Arquitetura](architecture.md).
Para uso, veja [Uso](usage.md).
Para resolução de problemas, veja [Resolução de Problemas](troubleshooting.md).
Para desenvolvimento futuro, veja [Desenvolvimento Futuro](future.md).
Voltar para o [Sumário](README.md).
