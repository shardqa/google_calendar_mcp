# Instalação

## Requisitos

- Python 3.8 ou superior
- Conta Google com acesso ao Google Calendar
- Credenciais OAuth2 do Google Cloud Platform

## Passos

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/google_calendar_mcp.git
   cd google_calendar_mcp
   ```
2. Configure o ambiente virtual:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # ou
   .venv\Scripts\activate      # Windows
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure as credenciais:
   - Crie um projeto no [Google Cloud Console](https://console.cloud.google.com/).
   - Ative a API do Google Calendar.
   - Crie credenciais OAuth2 para aplicativo desktop.
   - Baixe o arquivo JSON das credenciais como `credentials.json`.
   - Coloque-o na raiz do projeto. 

---
Para visão geral, veja [Visão Geral](overview.md).
Para arquitetura, veja [Arquitetura](architecture.md).
Para uso, veja [Uso](usage.md).
Para resolução de problemas, veja [Resolução de Problemas](troubleshooting.md).
Para desenvolvimento futuro, veja [Desenvolvimento Futuro](future.md).
Voltar para o [Sumário](README.md). 