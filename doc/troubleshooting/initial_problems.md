# Problemas Iniciais

Chamadas de ferramentas (`list_events`, etc.) retornavam erro de ferramenta não encontrada ou dados inválidos.

O cliente MCP não registrava as ferramentas porque o `mcp/hello` enviava `"capabilities.tools": {}` vazio.

O tool `list_events` retornava `invalid type expected array received undefined` (`["content"]`) porque a resposta JSON não incluía a chave `"content"` com um array de eventos.

Após corrigir o erro acima, o tool `list_events` retornava erros como `invalid literal expected text` e `invalid_type expected string received undefined` (`["content", 0, "text"]`), indicando que a estrutura dos itens dentro do array `"content"` não correspondia ao esperado (esperava objetos com chaves `"type": "text"` e `"text": "..."`).

Mesmo com a estrutura correta, o `list_events` retornava eventos antigos repetidos, em vez dos próximos eventos a partir da data/hora atual.

## Documentação Relacionada

- [Índice de Resolução de Problemas](../TROUBLESHOOTING.md)
- [Passos de Diagnóstico](diagnostic_steps.md)
- [Correções Aplicadas](applied_corrections.md)
- [Visão Geral](../../guides/overview.md)
- [Arquitetura](../../guides/architecture.md)
