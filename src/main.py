from datetime import datetime
from typing import Dict, List, Optional

from .auth import get_calendar_service
from .calendar_ops import CalendarOperations
from .cli import CLI

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