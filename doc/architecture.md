# Arquitetura do Projeto

## Estrutura de Diretórios

```
google_calendar_mcp/
├── config/               # Configurações do projeto
├── doc/                  # Documentação
├── src/                  # Código-fonte
│   ├── __init__.py
│   ├── auth.py           # Gerenciamento de autenticação
│   ├── calendar_ops.py   # Operações do calendário
│   ├── cli.py            # Interface de linha de comando
│   └── main.py           # Ponto de entrada da aplicação
├── tests/                # Testes automatizados
│   ├── test_auth.py
│   ├── test_calendar_ops.py
│   ├── test_cli.py
│   └── test_main.py
├── .coveragerc           # Configuração de cobertura de código
├── .gitignore            # Arquivos ignorados pelo git
├── credentials.json      # Credenciais OAuth2 (não versionado)
├── README.md             # Documentação principal
├── requirements.txt      # Dependências do projeto
└── token.pickle          # Token de autenticação (não versionado)
```

## Componentes Principais

### Módulo de Autenticação (`auth.py`)

- Estabelece a conexão OAuth2 com o Google
- Gerencia tokens de autenticação
- Persiste as credenciais entre sessões
- Renova tokens expirados automaticamente

### Operações de Calendário (`calendar_ops.py`)

- `list_events()`: Obtém a lista de eventos do calendário
- `add_event()`: Adiciona um novo evento ao calendário
- `remove_event()`: Remove um evento existente

### Interface de Linha de Comando (`cli.py`)

- Menu interativo para o usuário
- Processamento de argumentos de linha de comando
- Exibição formatada dos eventos
- Captura de entradas do usuário

### Módulo Principal (`main.py`)

- Ponto de entrada da aplicação
- Integração entre os componentes
- Fluxo de execução principal

---
Para visão geral, veja [Visão Geral](overview.md).
Para instalação, veja [Instalação](installation.md).
Para uso, veja [Uso](usage.md).
Para resolução de problemas, veja [Resolução de Problemas](troubleshooting.md).
Para desenvolvimento futuro, veja [Desenvolvimento Futuro](future.md).
Voltar para o [Sumário](README.md). 