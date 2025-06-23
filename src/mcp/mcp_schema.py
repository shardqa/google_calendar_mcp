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
                "name": "list_tasks",
                "description": "List pending tasks from Google Tasks",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "tasklist_id": {
                            "type": "string",
                            "description": "Task list ID (optional, defaults to @default)"
                        }
                    },
                    "required": []
                }
            },
            {
                "name": "add_task",
                "description": "Add a new task to Google Tasks",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "Title of the task"
                        },
                        "notes": {
                            "type": "string",
                            "description": "Notes or description of the task"
                        },
                        "due": {
                            "type": "string",
                            "description": "Due date (ISO format: YYYY-MM-DDTHH:MM:SS)"
                        },
                        "tasklist_id": {
                            "type": "string",
                            "description": "Task list ID (optional, defaults to @default)"
                        }
                    },
                    "required": ["title"]
                }
            },
            {
                "name": "remove_task",
                "description": "Remove a task from Google Tasks",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "task_id": {
                            "type": "string",
                            "description": "ID of the task to remove"
                        },
                        "tasklist_id": {
                            "type": "string",
                            "description": "Task list ID (optional, defaults to @default)"
                        }
                    },
                    "required": ["task_id"]
                }
            },
            {
                "name": "add_recurring_task",
                "description": "Add a recurring task/event to Google Calendar",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "summary": {
                            "type": "string",
                            "description": "Title of the recurring task"
                        },
                        "frequency": {
                            "type": "string",
                            "description": "Recurrence frequency (daily, weekly, monthly)",
                            "enum": ["daily", "weekly", "monthly"]
                        },
                        "count": {
                            "type": "integer",
                            "description": "Number of occurrences"
                        },
                        "start_time": {
                            "type": "string",
                            "description": "Start time (ISO format: YYYY-MM-DDTHH:MM:SS)"
                        },
                        "end_time": {
                            "type": "string",
                            "description": "End time (ISO format: YYYY-MM-DDTHH:MM:SS)"
                        },
                        "location": {
                            "type": "string",
                            "description": "Location of the task (optional)"
                        },
                        "description": {
                            "type": "string",
                            "description": "Description of the task (optional)"
                        }
                    },
                    "required": ["summary", "frequency", "count", "start_time", "end_time"]
                }
            },
            {
                "name": "schedule_tasks",
                "description": "Intelligently schedule tasks based on calendar availability and task priorities",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "time_period": {
                            "type": "string",
                            "description": "Time period for scheduling",
                            "enum": ["day", "week", "month"]
                        },
                        "work_hours_start": {
                            "type": "string",
                            "description": "Work hours start time (HH:MM format)"
                        },
                        "work_hours_end": {
                            "type": "string",
                            "description": "Work hours end time (HH:MM format)"
                        },
                        "max_task_duration": {
                            "type": "integer",
                            "description": "Maximum task duration in minutes (default: 120)"
                        }
                    },
                    "required": ["time_period", "work_hours_start", "work_hours_end"]
                }
            }
        ]
    } 