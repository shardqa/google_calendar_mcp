# Intelligent Scheduling System

## Business Rule

Enable users to request automatic agenda scheduling based on their current tasks
and commitments. The system should analyze existing calendar events and task
lists, then propose optimal time blocks for task completion.

## Core Functionality

### Primary Use Case

User request: "Schedule my tasks for this week based on my current agenda and priorities"

### System Response Process

1. **Read Current State**
   - Fetch all calendar events for specified time period
   - Retrieve all pending tasks from Google Tasks
   - Analyze task priorities, deadlines, and estimated durations

2. **Intelligent Analysis**
   - Identify available time slots in calendar
   - Order tasks by priority algorithm (deadline + importance)
   - Match task duration requirements with available time blocks
   - Consider user preferences (work hours, break intervals)

3. **Schedule Proposal**
   - Generate time block suggestions for each high-priority task
   - Create calendar events for proposed task blocks
   - Provide scheduling rationale and alternatives

## Algorithm Specifications

### Priority Calculation

```python
priority_score = (deadline_urgency * 0.4) + (user_importance * 0.3) + \
                 (estimated_effort * 0.3)
```

### Time Block Matching

- Minimum task block: 30 minutes
- Maximum continuous work block: 2 hours
- Buffer time between tasks: 15 minutes
- Respect existing calendar commitments

## MCP Commands

### `schedule_tasks`

**Input Parameters:**

- `time_period`: "week" | "day" | "month"
- `work_hours_start`: "09:00"
- `work_hours_end`: "18:00"
- `max_task_duration`: 120 (minutes)

**Output:**

- List of proposed calendar events for tasks
- Scheduling summary with rationale
- Alternative time slots for each task

## Implementation Status

### Core Engine (`src/core/scheduling_engine.py`)

✅ **Implemented Features:**

- **Calendar Analysis**: Fetches events for specified time periods (day/week/month)
- **Task Integration**: Retrieves pending tasks from Google Tasks
- **Gap Detection**: Identifies available time slots between existing events
- **Intelligent Filtering**: Excludes slots smaller than 30 minutes
- **Work Hours Respect**: Honors configured start/end work times
- **Duration Matching**: Matches task duration with available slots

✅ **Algorithm Logic:**

```python
def analyze_schedule(time_period, work_hours_start, work_hours_end):
    calendar_events = _get_calendar_events(time_period)
    pending_tasks = _get_pending_tasks()
    available_slots = _find_available_slots(events, work_hours)
    return analysis_result

def propose_schedule(time_period, max_task_duration):
    analysis = analyze_schedule(time_period, work_hours)
    proposed_events = _create_task_events(slots, tasks, max_duration)
    return scheduling_proposal
```

✅ **MCP Integration:**

- Command `schedule_tasks` available via Server-Sent Events
- Full JSON-RPC 2.0 compatibility
- Error handling for service failures
- Real-time streaming for long operations

### Quality Assurance

✅ **100% Test Coverage:**

- **30+ dedicated tests** for scheduling engine
- **Edge case coverage**: Empty calendars, conflicting events, short gaps
- **Error scenarios**: Service failures, malformed data, network issues
- **Branch coverage**: All conditional logic paths tested
- **Integration tests**: End-to-end MCP command flow

## Integration Points

For implementation details, see [Architecture](architecture.md) and
[Usage](usage.md) documentation.
