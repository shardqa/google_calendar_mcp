def get_mcp_schema():
    return {
        "name": "google_calendar",
        "description": "Google Calendar Tool for viewing and managing calendar events",
        "protocol": "2025-03-26",
        "serverInfo": {
            "name": "google_calendar",
            "version": "1.0.0"
        },
        "tools": [
            {
                "name": "echo",
                "description": "Echo back the input message",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": "Message to echo"
                        }
                    },
                    "required": ["message"]
                }
            },
            {
                "name": "list_events",
                "description": "List upcoming events from Google Calendar",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "max_results": {
                            "type": "integer",
                            "description": "Maximum number of events to return"
                        }
                    },
                    "required": []
                }
            },
            {
                "name": "add_event",
                "description": "Add a new event to Google Calendar",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "summary": {
                            "type": "string",
                            "description": "Title of the event"
                        },
                        "location": {
                            "type": "string",
                            "description": "Location of the event"
                        },
                        "description": {
                            "type": "string",
                            "description": "Description of the event"
                        },
                        "start_time": {
                            "type": "string",
                            "description": "Start time (ISO format: YYYY-MM-DDTHH:MM:SS)"
                        },
                        "end_time": {
                            "type": "string",
                            "description": "End time (ISO format: YYYY-MM-DDTHH:MM:SS)"
                        }
                    },
                    "required": ["summary", "start_time", "end_time"]
                }
            },
            {
                "name": "remove_event",
                "description": "Remove an event from Google Calendar",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "event_id": {
                            "type": "string",
                            "description": "ID of the event to remove"
                        }
                    },
                    "required": ["event_id"]
                }
            }
        ]
    } 