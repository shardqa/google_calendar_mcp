# Monitoramento & Manutenção

## Verificação de Saúde

```bash
curl http://10.243.215.33:3001/health
python -m src.mcp_cli --port 3001 --host 10.243.215.33
```

## Logs

```bash
sudo systemctl status google-calendar-mcp
sudo journalctl -u google-calendar-mcp -f
```

## Procedimentos de Manutenção

```bash
sudo systemctl restart google-calendar-mcp       # restart serviço
git -C /path/to/google_calendar_mcp pull origin main
find . -name "*.pyc" -delete                     # limpar cache
```

---

Veja também: [Troubleshooting](troubleshooting.md) · [Security Plan](../security_plan.md)
