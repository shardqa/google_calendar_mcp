# Google Calendar MCP

Servidor MCP (Model Context Protocol) completo para integração de Google Calendar e Google Tasks com assistentes de IA. Oferece interface unificada para gerenciamento de eventos e tarefas, com suporte a execução local e remota.

## Características Principais

- **Gerenciamento de Calendário**: Listar, adicionar e remover eventos
- **Integração Google Tasks**: Operações completas de CRUD para tarefas
- **Servidor MCP Remoto**: Execução como serviço via systemd
- **Alta Confiabilidade**: 99% de cobertura de testes com 182 testes automatizados
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

O módulo suporta execução como servidor MCP para integração com Cursor AI e outras ferramentas compatíveis.

Para iniciar o servidor MCP local:

```bash
python -m src.mcp_cli
```

Opções disponíveis:

- `--port PORT`: Porta para executar o servidor (padrão: 3000)
- `--host HOST`: Host para o servidor (padrão: localhost)
- `--setup-only`: Apenas configurar o arquivo MCP sem iniciar o servidor

O comando irá automaticamente configurar o arquivo `.cursor/mcp.json` com as informações do servidor.

### Ferramentas Disponíveis via MCP

**Calendário:**
- `list_events`: Listar eventos próximos
- `add_event`: Criar novos eventos com título, descrição, horário e localização
- `remove_event`: Remover eventos existentes

**Tarefas (Google Tasks):**
- `list_tasks`: Listar tarefas pendentes
- `add_task`: Criar tarefas com título, notas e prazo
- `remove_task`: Marcar tarefas como concluídas

**Utilitários:**
- `echo`: Teste de conectividade e validação

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
