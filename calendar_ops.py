from datetime import datetime, timedelta
from dateutil import parser
from typing import List, Dict, Optional, Union

class CalendarError(Exception):
    """Exceção base para erros relacionados ao calendário."""
    pass

class EventValidationError(CalendarError):
    """Exceção para erros de validação de eventos."""
    pass

def validate_datetime(dt_str: str) -> datetime:
    """
    Valida e converte uma string de data/hora para objeto datetime.
    
    Args:
        dt_str: String de data/hora no formato DD/MM/AAAA HH:MM
    
    Returns:
        Objeto datetime
        
    Raises:
        EventValidationError: Se o formato da data/hora for inválido
    """
    try:
        return datetime.strptime(dt_str, '%d/%m/%Y %H:%M')
    except ValueError:
        raise EventValidationError("Formato de data/hora inválido. Use DD/MM/AAAA HH:MM")

def list_events(service, max_results: int = 10) -> List[Dict]:
    """
    Lista os próximos eventos do calendário.
    
    Args:
        service: Serviço do Google Calendar
        max_results: Número máximo de eventos a retornar (1-100)
    
    Returns:
        Lista de eventos
    
    Raises:
        CalendarError: Se houver erro ao listar eventos
    """
    if not 1 <= max_results <= 100:
        raise EventValidationError("max_results deve estar entre 1 e 100")
        
    try:
        now = datetime.utcnow().isoformat() + 'Z'
        events_result = service.events().list(
            calendarId='primary',
            timeMin=now,
            maxResults=max_results,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        return events_result.get('items', [])
    except Exception as e:
        raise CalendarError(f"Erro ao listar eventos: {str(e)}")

def add_event(service, title: str, description: str, start_time: str, end_time: str) -> Optional[Dict]:
    """
    Adiciona um novo evento ao calendário.
    
    Args:
        service: Serviço do Google Calendar
        title: Título do evento
        description: Descrição do evento
        start_time: Data/hora de início (formato DD/MM/AAAA HH:MM)
        end_time: Data/hora de término (formato DD/MM/AAAA HH:MM)
    
    Returns:
        Evento criado ou None em caso de erro
        
    Raises:
        EventValidationError: Se os dados do evento forem inválidos
        CalendarError: Se houver erro ao adicionar evento
    """
    if not title.strip():
        raise EventValidationError("O título do evento não pode estar vazio")
        
    try:
        start_dt = validate_datetime(start_time)
        end_dt = validate_datetime(end_time)
        
        if end_dt <= start_dt:
            raise EventValidationError("A data/hora de término deve ser posterior à data/hora de início")
            
        event = {
            'summary': title,
            'description': description,
            'start': {
                'dateTime': start_dt.isoformat(),
                'timeZone': 'America/Sao_Paulo',
            },
            'end': {
                'dateTime': end_dt.isoformat(),
                'timeZone': 'America/Sao_Paulo',
            },
        }

        event = service.events().insert(
            calendarId='primary',
            body=event
        ).execute()
        
        return event
    except EventValidationError:
        raise
    except Exception as e:
        raise CalendarError(f"Erro ao adicionar evento: {str(e)}")

def delete_event(service, event_id: str) -> bool:
    """
    Remove um evento do calendário.
    
    Args:
        service: Serviço do Google Calendar
        event_id: ID do evento a ser removido
    
    Returns:
        True se o evento foi removido com sucesso
        
    Raises:
        EventValidationError: Se o ID do evento for inválido
        CalendarError: Se houver erro ao remover evento
    """
    if not event_id.strip():
        raise EventValidationError("ID do evento não pode estar vazio")
        
    try:
        service.events().delete(
            calendarId='primary',
            eventId=event_id
        ).execute()
        return True
    except Exception as e:
        raise CalendarError(f"Erro ao remover evento: {str(e)}") 