from datetime import datetime
from typing import Dict, List, Optional

class CLI:
    def __init__(self, calendar_ops):
        self.calendar_ops = calendar_ops

    def display_menu(self) -> None:
        """Display the main menu options."""
        print("\nGoogle Calendar MCP")
        print("1. List Events")
        print("2. Add Event")
        print("3. Remove Event")
        print("4. Exit")

    def process_command(self, command: str) -> bool:
        """
        Process the user command.
        
        Args:
            command: The user's command input
            
        Returns:
            bool: False if the user wants to exit, True otherwise
        """
        if command == "1":
            events = self.calendar_ops.list_events()
            if events:
                for event in events:
                    start = event.get('start', {}).get('dateTime', 'N/A')
                    print(f"{event['summary']} - {start}")
            else:
                print("No upcoming events found.")
            return True
            
        elif command == "2":
            summary = input("Event title: ")
            start_date = input("Start date and time (YYYY-MM-DD HH:MM): ")
            end_date = input("End date and time (YYYY-MM-DD HH:MM): ")
            
            try:
                start = datetime.strptime(start_date, "%Y-%m-%d %H:%M")
                end = datetime.strptime(end_date, "%Y-%m-%d %H:%M")
                
                event = {
                    'summary': summary,
                    'start': {'dateTime': start.isoformat()},
                    'end': {'dateTime': end.isoformat()}
                }
                
                result = self.calendar_ops.add_event(event)
                if result.get('status') == 'confirmed':
                    print("Event added successfully!")
                else:
                    print("Failed to add event.")
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD HH:MM")
            return True
            
        elif command == "3":
            event_id = input("Enter event ID to remove: ")
            if self.calendar_ops.remove_event(event_id):
                print("Event removed successfully!")
            else:
                print("Failed to remove event.")
            return True
            
        elif command == "4":
            print("Goodbye!")
            return False
            
        else:
            print("Invalid command. Please try again.")
            return True

    def run_interactive_loop(self) -> None:
        """Run the interactive command loop."""
        running = True
        while running:
            self.display_menu()
            command = input("\nEnter your choice (1-4): ")
            running = self.process_command(command) 