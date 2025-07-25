# Google Calendar MCP

Servidor MCP (Model Context Protocol) completo para integração de Google
Calendar e Google Tasks com assistentes de IA. Oferece interface unificada para
gerenciamento de eventos e tarefas, com suporte a execução local e remota.

## Características Principais

- **Gerenciamento de Calendário**: Listar, adicionar e remover eventos.
- **Integração Google Tasks**: Operações completas de CRUD para tarefas.
- **Agendamento Inteligente**: Análise automática de agenda e proposição de horários.
- **Servidor MCP Remoto**: Execução como serviço via `systemd`.
- **Alta Confiabilidade**: 90% de cobertura de testes com 279+ testes automatizados.
- **CI/CD Automatizada**: Pipeline GitHub Actions com deployment contínuo.

## Documentação

A documentação completa está dividida em guias específicos para facilitar a consulta.

- **[Visão Geral](doc/guides/overview.md)**: Comece por aqui para uma introdução ao projeto.
- **[Instalação](doc/guides/installation.md)**: Guia completo para configurar o ambiente.
- **[Arquitetura](doc/guides/architecture.md)**: Detalhes sobre a estrutura modular do projeto.
- **[Ferramentas MCP](doc/guides/mcp_tools.md)**: Lista e descrição de todas as ferramentas disponíveis.
- **[Exemplos de Uso](doc/guides/usage_examples.md)**: Cenários práticos e fluxos de trabalho.
- **[Boas Práticas de Refatoração](doc/guides/refactoring_best_practices.md)**: Lições aprendidas com a modularização.
- **[Contribuição](doc/guides/contributing.md)**: Como contribuir para o projeto.
- **[Índice Completo](doc/README.md)**: Navegue por todos os documentos.

## Uso Rápido

Após seguir o guia de **[Instalação](doc/guides/installation.md)**, você pode iniciar o servidor MCP localmente:

```bash
python -m src.commands.mcp_cli --port 3000
```

Isso ativará as ferramentas para serem usadas por clientes compatíveis, como o Cursor.

---
Para detalhes sobre a licença, veja a seção no [Guia de Contribuição](doc/guides/contributing.md).
