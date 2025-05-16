from .core.auth import get_calendar_service
from .core.calendar_ops import CalendarOperations
from .commands.cli import CLI

def main():
    try:
        service = get_calendar_service()
        calendar_ops = CalendarOperations(service)
        cli = CLI(calendar_ops)
        cli.run_interactive_loop()
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    return 0

if __name__ == "__main__":
    exit(main()) 