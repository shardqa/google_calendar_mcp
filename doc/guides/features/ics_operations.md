# ICS External Calendar Operations

## Overview

The Google Calendar MCP supports external ICS calendars with robust error
handling and debug capabilities. This integration allows users to access events
from any ICS-compatible calendar service alongside their Google Calendar events.

## Enhanced Error Handling

### Network Resilience

The system now gracefully handles common network issues:

- **Connection timeouts**: Returns informative error messages instead of crashing
- **DNS resolution failures**: Clear feedback about unreachable hosts
- **HTTP errors**: Proper handling of 404, 500, and other status codes
- **SSL certificate issues**: Helpful messages for HTTPS problems

### Data Validation

- **Malformed ICS data**: Attempts to parse partial data and reports issues
- **Empty calendars**: Distinguishes between network errors and empty calendars
- **Invalid date formats**: Skips problematic events with warnings
- **Encoding issues**: Handles different character encodings gracefully

## Debug Mode

### Enabling Debug Information

```python
# Enable debug mode for detailed information
events = list_events(ics_url="https://example.com/calendar.ics", debug=True)
```

### Debug Output Examples

**Successful processing with filtering:**

```text
📅 ICS Calendar Debug Info:
- Fetched 15 events from calendar
- Filtered out 12 past events
- Returning 3 upcoming events
- Next event: "Team Meeting" on 2025-01-03
```

**Network error scenario:**

```text
❌ Failed to fetch ICS calendar from https://broken.example.com/calendar.ics:
- Error: Connection timeout after 10 seconds
- Suggestion: Check URL and network connectivity
```

**Empty calendar scenario:**

```text
📅 No events found in ICS calendar
- Calendar successfully fetched but contains no events
- Or all events were filtered (past dates)
- Use debug=True for more details
```

## Common Issues and Solutions

### Issue: No Events Returned

**Symptoms**: Calendar appears empty despite having events

**Possible Causes**:

1. All events are in the past (filtered by default)
2. Network connectivity issues
3. Incorrect ICS URL
4. Calendar requires authentication

**Troubleshooting Steps**:

```bash
# 1. Test with debug mode
python -m src.commands.mcp_cli list-events --ics-url="URL" --debug

# 2. Test network connectivity
curl -I "https://example.com/calendar.ics"

# 3. Check ICS format manually
curl "https://example.com/calendar.ics" | head -20
```

### Issue: Slow Response Times

**Solutions**:

- Use `fetch_timeout` parameter to adjust timeout
- Consider caching for frequently accessed calendars
- Check if the calendar source supports HTTP compression

### Issue: Encoding Problems

**Symptoms**: Special characters appear garbled

**Solutions**:

- The system automatically handles UTF-8 and common encodings
- For persistent issues, check the calendar source's encoding headers
- Use debug mode to see encoding information

## Best Practices

### URL Formats

**Supported formats**:

- `https://calendar.google.com/calendar/ical/...`
- `webcal://example.com/calendar.ics` (converted to https://)
- `http://internal-server/calendar.ics`

### Performance Optimization

- **Caching**: Consider implementing local caching for static calendars
- **Filtering**: Use date ranges to limit processed events
- **Timeouts**: Adjust `fetch_timeout` based on network conditions

### Error Recovery

The system provides multiple fallback strategies:

1. **Partial parsing**: Attempts to extract valid events even from problematic calendars
2. **Graceful degradation**: Returns error messages that users can understand
3. **Debug information**: Detailed logging for troubleshooting

## Integration with MCP Tools

### Available MCP Functions

- `mcp_google_calendar_list_events` with `ics_url` parameter
- `mcp_google_calendar_register_ics_calendar` for alias management
- `mcp_google_calendar_list_ics_calendars` to view registered aliases

### Usage in Cursor

```json
{
  "name": "mcp_google_calendar_list_events",
  "arguments": {
    "ics_url": "https://example.com/calendar.ics",
    "max_results": 10
  }
}
```

## Technical Implementation

### Error Handling Flow

```python
def list_events(self, ics_url: str, debug: bool = False):
    try:
        ics_text = self._download_ics(ics_url)
    except Exception as e:
        error_msg = f"❌ Failed to fetch ICS calendar from {ics_url}: {str(e)}"
        return [{"type": "text", "text": error_msg}]
    
    # Continue with parsing and filtering...
```

### Debug Information Structure

Debug mode provides structured information:

- **Fetch status**: Network operation results
- **Parse status**: ICS data validation results  
- **Filter status**: Event filtering explanations
- **Final status**: Summary of returned events

---

For installation, see [Installation](../setup/installation.md).
For architecture, see [Architecture](../architecture/overview.md).
For troubleshooting, see [Troubleshooting](../../troubleshooting.md).
Back to [README](../../README.md).
