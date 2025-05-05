import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Escopo necessário para acessar o Google Calendar
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_credentials():
    """
    Obtém as credenciais do Google Calendar API.
    Se não existirem tokens salvos, inicia o fluxo de autenticação OAuth2.
    """
    creds = None
    token_path = 'token.pickle'

    # Tenta carregar tokens salvos
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    # Se não há credenciais válidas, solicita nova autenticação
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Salva as credenciais para uso futuro
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    return creds

def get_calendar_service():
    """
    Estabelece conexão com a API do Google Calendar.
    Retorna o serviço configurado.
    """
    try:
        creds = get_credentials()
        service = build('calendar', 'v3', credentials=creds)
        return service
    except Exception as e:
        print(f"Erro ao estabelecer conexão com o Google Calendar: {e}")
        raise 