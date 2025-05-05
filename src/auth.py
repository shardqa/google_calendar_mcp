import json
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/calendar']

def load_credentials(path):
    """
    Carrega as credenciais OAuth2 do arquivo JSON.
    
    Args:
        path (str): Caminho para o arquivo de credenciais

    Returns:
        dict: Credenciais carregadas do arquivo

    Raises:
        FileNotFoundError: Se o arquivo não for encontrado
        ValueError: Se o arquivo JSON for inválido
    """
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f'Arquivo de credenciais não encontrado: {path}')
    except json.JSONDecodeError:
        raise ValueError(f'Arquivo de credenciais inválido: {path}')

def get_token(path):
    """
    Obtém um token de acesso OAuth2 para o Google Calendar.
    
    Args:
        path (str): Caminho para o arquivo de credenciais

    Returns:
        str: Token de acesso em formato JSON

    Raises:
        FileNotFoundError: Se o arquivo de credenciais não for encontrado
        ValueError: Se o arquivo de credenciais for inválido
        Exception: Se houver erro no fluxo de autenticação
    """
    try:
        creds = load_credentials(path)
        flow = InstalledAppFlow.from_client_secrets_file(path, SCOPES)
        creds = flow.run_local_server(port=0)
        return creds.to_json()
    except (FileNotFoundError, ValueError) as e:
        raise e
    except Exception as e:
        raise Exception(f'Erro ao obter token: {str(e)}') 