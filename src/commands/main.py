from datetime import datetime
from typing import Dict, List, Optional

from ..core.auth import get_calendar_service
from ..core.calendar_ops import CalendarOperations
from .cli import CLI
import src.main as app

def main():
    return app.main()

if __name__ == "__main__": # pragma: no cover
    exit(main()) 