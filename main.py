import sys
from datetime import datetime
from dateutil import parser
from auth import get_calendar_service
from calendar_ops import (
    list_events, add_event, delete_event,
    CalendarError, EventValidationError
)

def print_menu():
    """Exibe o menu principal do programa."""
    print("\n=== Google Calendar MCP ===")
    print("1. Listar próximos eventos")
    print("2. Adicionar novo evento")
    print("3. Remover evento")
    print("4. Sair")
    print("=========================")

def format_event(event):
    """Formata um evento para exibição."""
    start = parser.parse(event['start'].get('dateTime', event['start'].get('date')))
    end = parser.parse(event['end'].get('dateTime', event['end'].get('date')))
    
    return f"""
ID: {event['id']}
Título: {event['summary']}
Início: {start.strftime('%d/%m/%Y %H:%M')}
Término: {end.strftime('%d/%m/%Y %H:%M')}
Descrição: {event.get('description', 'N/A')}
{'=' * 40}"""

def get_max_results():
    """Solicita e valida o número máximo de eventos a serem listados."""
    while True:
        try:
            max_results = int(input("Quantos eventos deseja listar? (1-100): "))
            if 1 <= max_results <= 100:
                return max_results
            print("Por favor, insira um número entre 1 e 100.")
        except ValueError:
            print("Por favor, insira um número válido.")

def handle_list_events(service):
    """Manipula a listagem de eventos."""
    try:
        max_results = get_max_results()
        events = list_events(service, max_results)
        
        if events:
            print(f"\nPróximos {len(events)} eventos:")
            for event in events:
                print(format_event(event))
        else:
            print("\nNenhum evento encontrado.")
    except CalendarError as e:
        print(f"\nErro: {e}")

def handle_add_event(service):
    """Manipula a adição de um novo evento."""
    try:
        print("\n=== Adicionar Novo Evento ===")
        title = input("Título do evento: ").strip()
        description = input("Descrição: ").strip()
        start_str = input("Data/hora de início (DD/MM/AAAA HH:MM): ").strip()
        end_str = input("Data/hora de término (DD/MM/AAAA HH:MM): ").strip()
        
        event = add_event(service, title, description, start_str, end_str)
        if event:
            print("\nEvento adicionado com sucesso!")
            print(format_event(event))
    except (CalendarError, EventValidationError) as e:
        print(f"\nErro: {e}")

def handle_delete_event(service):
    """Manipula a remoção de um evento."""
    try:
        print("\n=== Remover Evento ===")
        event_id = input("ID do evento a ser removido: ").strip()
        
        if delete_event(service, event_id):
            print("\nEvento removido com sucesso!")
    except (CalendarError, EventValidationError) as e:
        print(f"\nErro: {e}")

def main():
    """Função principal do programa."""
    try:
        print("Iniciando Google Calendar MCP...")
        print("Estabelecendo conexão com o Google Calendar...")
        service = get_calendar_service()
        print("Conexão estabelecida com sucesso!")
        
        while True:
            print_menu()
            choice = input("\nEscolha uma opção: ").strip()
            
            if choice == '1':
                handle_list_events(service)
            elif choice == '2':
                handle_add_event(service)
            elif choice == '3':
                handle_delete_event(service)
            elif choice == '4':
                print("\nEncerrando programa...")
                sys.exit(0)
            else:
                print("\nOpção inválida! Por favor, escolha uma opção de 1 a 4.")
                
    except KeyboardInterrupt:
        print("\n\nPrograma interrompido pelo usuário.")
        sys.exit(0)
    except Exception as e:
        print(f"\nErro fatal: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 