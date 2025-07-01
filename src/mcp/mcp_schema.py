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
                "name": "list_events",
                "description": "List upcoming events from Google Calendar or an external ICS URL",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "max_results": {
                            "type": "integer",
                            "description": "Maximum number of events to return"
                        },
                        "calendar_id": {
                            "type": "string",
                            "description": "ID of the Google Calendar to query (defaults to primary)"
                        },
                        "ics_url": {
                            "type": "string",
                            "description": "External ICS URL to fetch events from (takes precedence over calendar_id)"
                        },
                        "ics_alias": {
                            "type": "string",
                            "description": "Alias of a previously registered ICS calendar URL"
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
            },
            {
                "name": "edit_event",
                "description": "Edit an existing event in Google Calendar",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "event_id": {
                            "type": "string",
                            "description": "ID of the event to edit"
                        },
                        "updated_details": {
                            "type": "object",
                            "description": "Updated event details (summary, location, description, start/end times)",
                            "properties": {
                                "summary": {
                                    "type": "string",
                                    "description": "New title of the event"
                                },
                                "location": {
                                    "type": "string",
                                    "description": "New location of the event"
                                },
                                "description": {
                                    "type": "string",
                                    "description": "New description of the event"
                                },
                                "start": {
                                    "type": "object",
                                    "properties": {
                                        "dateTime": {
                                            "type": "string",
                                            "description": "New start time (ISO format)"
                                        }
                                    }
                                },
                                "end": {
                                    "type": "object",
                                    "properties": {
                                        "dateTime": {
                                            "type": "string",
                                            "description": "New end time (ISO format)"
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "required": ["event_id", "updated_details"]
                }
            },
            {
                "name": "register_ics_calendar",
                "description": "Register a persistent alias for an external ICS calendar URL",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "alias": {"type": "string", "description": "Short alias"},
                        "ics_url": {"type": "string", "description": "ICS URL to associate"}
                    },
                    "required": ["alias", "ics_url"]
                }
            },
            {
                "name": "list_ics_calendars",
                "description": "List registered ICS calendar aliases",
                "inputSchema": {"type": "object", "properties": {}, "required": []}
            }
        ]
    } 