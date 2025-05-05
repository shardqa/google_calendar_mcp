# Google Calendar MCP (Módulo de Comando de Processamento)

Um módulo de linha de comando para gerenciar eventos no Google Calendar de forma simples e eficiente.

## Funcionalidades

- Listar próximos eventos do calendário
- Adicionar novos eventos com título, descrição, data e hora
- Remover eventos existentes
- Interface de linha de comando intuitiva
- Autenticação OAuth2 com o Google
- Gerenciamento automático de tokens

## Requisitos

- Python 3.8 ou superior
- Conta Google com acesso ao Google Calendar
- Credenciais OAuth2 do Google Cloud Platform

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/google_calendar_mcp.git
cd google_calendar_mcp
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as credenciais do Google:
   - Acesse o [Google Cloud Console](https://console.cloud.google.com)
   - Crie um novo projeto ou selecione um existente
   - Ative a API do Google Calendar
   - Crie credenciais OAuth2 para aplicativo desktop
   - Baixe o arquivo JSON das credenciais
   - Renomeie o arquivo para `credentials.json` e coloque-o na raiz do projeto

## Uso

1. Execute o programa:
```bash
python main.py
```

2. Na primeira execução, você será redirecionado para o navegador para autorizar o acesso ao seu Google Calendar.

3. Use o menu interativo para:
   - Listar próximos eventos
   - Adicionar novos eventos
   - Remover eventos existentes

## Estrutura do Projeto

```
google_calendar_mcp/
├── .gitignore
├── README.md
├── requirements.txt
├── main.py              # Interface de linha de comando
├── auth.py             # Autenticação com Google Calendar
├── calendar_ops.py     # Operações com eventos
└── credentials.json    # Credenciais OAuth2 (não versionado)
```

## Tratamento de Erros

O MCP inclui tratamento robusto de erros para:
- Falhas de autenticação
- Entradas inválidas do usuário
- Erros de conexão com a API
- Formato de data/hora inválido
- IDs de eventos inexistentes

## Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Crie um Pull Request

## Licença

Este projeto está licenciado sob a MIT License - veja o arquivo LICENSE para detalhes. 