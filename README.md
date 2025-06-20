# Google Calendar MCP

Módulo de linha de comando para gerenciar eventos no Google Calendar de forma simples e eficiente.
Agora com suporte para integração como servidor MCP para Cursor AI e outras ferramentas.

## Documentação

- [Visão Geral](doc/overview.md)
- [Instalação](doc/installation.md)
- [Arquitetura](doc/architecture.md)
- [Uso](doc/usage.md)
- [Resolução de Problemas](doc/troubleshooting.md)
- [Desenvolvimento Futuro](doc/future.md)
- [Índice Completo](doc/README.md)

## Uso como Servidor MCP

O módulo agora suporta execução como um servidor MCP (Model Context Protocol) para integração com o Cursor AI.

Para iniciar o servidor MCP:

```bash
python -m src.mcp_cli
```

Opções disponíveis:

- `--port PORT`: Porta para executar o servidor (padrão: 3000)
- `--host HOST`: Host para o servidor (padrão: localhost)
- `--setup-only`: Apenas configurar o arquivo MCP sem iniciar o servidor

O comando irá automaticamente configurar o arquivo `.cursor/mcp.json` com as informações do servidor.

### Endpoints disponíveis via MCP

- `list_events`: Listar eventos do calendário
- `add_event`: Adicionar um novo evento
- `remove_event`: Remover um evento existente

## Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Crie um Pull Request

## Licença

Este projeto está licenciado sob a MIT License - veja o arquivo LICENSE para detalhes.
