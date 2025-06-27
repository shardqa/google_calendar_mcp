# APIs & Dependências Externas

## Google Cloud APIs Requeridas

1. **Google Calendar API** – habilitada, quota monitorada  
2. **Google Tasks API** – habilitada, scopes `auth/calendar` e `auth/tasks`

## Renovação de Tokens

O token (`token.pickle`) é renovado automaticamente. Para forçar nova
autenticação:

```bash
rm token.pickle
python -m src.cli auth
```

---

Veja também: [Security Plan](../security_plan.md) · [Tasks Integration](../tasks_integration.md)
