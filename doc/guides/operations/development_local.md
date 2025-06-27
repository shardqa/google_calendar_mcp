# Desenvolvimento Local

## Comandos Make Disponíveis

### Servidor MCP Local

```bash
make mcp-local      # iniciar servidor na porta 3001
make mcp-start      # iniciar servidor padrão
make mcp-stop       # parar servidor
make mcp-restart    # reiniciar servidor
```

### Testes e Qualidade

```bash
make test        # testes completos + cobertura
make test-fast   # testes rápidos sem cobertura
make clean       # limpar artefatos temporários
make help        # lista de comandos disponíveis
```

## Fluxo de Desenvolvimento Recomendado

1. Alterar o código desejado  
2. Executar `make test` para garantir 100 % de cobertura  
3. Executar `make mcp-local` para testes locais  
4. Validar no Cursor IDE  
5. Commit e push para deploy automático

---

Veja também: [Testes](../installation.md) · [Development Best Practices](../development_best_practices.md)
