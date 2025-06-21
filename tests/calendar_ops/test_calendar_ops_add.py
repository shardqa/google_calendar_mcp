import pytest

def test_add_event_success(calendar_ops, mock_service):
    event_data = {
        'summary': 'Test Event',
        'start': {'dateTime': '2024-03-20T10:00:00Z'},
        'end': {'dateTime': '2024-03-20T11:00:00Z'}
    }
    events_mock = mock_service.events.return_value
    events_mock.insert.return_value.execute.return_value = event_data
    result = calendar_ops.add_event(event_data)
    assert result['status'] == 'confirmed'
    assert result['event'] == event_data
    mock_service.events.assert_called_once()
    events_mock.insert.assert_called_once()
    events_mock.insert.return_value.execute.assert_called_once()

def test_add_event_failure(calendar_ops, mock_service):
    event_data = {
        'summary': 'Test Event',
        'start': {'dateTime': 'invalid-date'},
        'end': {'dateTime': 'invalid-date'}
    }
    events_mock = mock_service.events.return_value
    events_mock.insert.return_value.execute.side_effect = Exception("Invalid date format")
    result = calendar_ops.add_event(event_data)
    assert result['status'] == 'error'
    assert 'message' in result
    mock_service.events.assert_called_once()
    events_mock.insert.assert_called_once()
    events_mock.insert.return_value.execute.assert_called_once()

def test_add_recurring_event_daily(calendar_ops, mock_service):
    """Test that add_recurring_event creates daily recurring events."""
    mock_event = {
        'id': 'recurring_daily_123',
        'status': 'confirmed',
        'summary': 'Tomar remédio',
        'recurrence': ['RRULE:FREQ=DAILY;COUNT=30']
    }
    events_mock = mock_service.events.return_value
    events_mock.insert.return_value.execute.return_value = mock_event
    
    result = calendar_ops.add_recurring_event(
        summary='Tomar remédio',
        frequency='daily',
        count=30,
        start_time='2024-03-20T08:00:00Z',
        end_time='2024-03-20T08:30:00Z'
    )
    
    assert result['status'] == 'confirmed'
    assert result['id'] == 'recurring_daily_123'
    
    # Verify the call was made with recurrence rule
    events_mock.insert.assert_called_once()
    call_args = events_mock.insert.call_args
    event_data = call_args[1]['body']
    
    assert event_data['summary'] == 'Tomar remédio'
    assert 'recurrence' in event_data
    assert 'RRULE:FREQ=DAILY;COUNT=30' in event_data['recurrence']

def test_add_recurring_event_weekly(calendar_ops, mock_service):
    """Test that add_recurring_event creates weekly recurring events."""
    mock_event = {
        'id': 'recurring_weekly_456', 
        'status': 'confirmed',
        'summary': 'Reunião semanal',
        'recurrence': ['RRULE:FREQ=WEEKLY;COUNT=10;BYDAY=MO']
    }
    events_mock = mock_service.events.return_value
    events_mock.insert.return_value.execute.return_value = mock_event
    
    result = calendar_ops.add_recurring_event(
        summary='Reunião semanal',
        frequency='weekly',
        count=10,
        start_time='2024-03-20T09:00:00Z',
        end_time='2024-03-20T10:00:00Z',
        location='Sala de reunião',
        description='Reunião semanal da equipe'
    )
    
    assert result['status'] == 'confirmed'
    assert result['id'] == 'recurring_weekly_456'
    
    # Verify the call was made with correct data
    events_mock.insert.assert_called_once()
    call_args = events_mock.insert.call_args
    event_data = call_args[1]['body']
    
    assert event_data['summary'] == 'Reunião semanal'
    assert event_data['location'] == 'Sala de reunião'
    assert event_data['description'] == 'Reunião semanal da equipe'
    assert 'recurrence' in event_data
    assert any('RRULE:FREQ=WEEKLY' in rule for rule in event_data['recurrence'])

def test_add_recurring_event_monthly(calendar_ops, mock_service):
    """Test that add_recurring_event creates monthly recurring events."""
    mock_event = {
        'id': 'recurring_monthly_789',
        'status': 'confirmed', 
        'summary': 'Pagamento mensal',
        'recurrence': ['RRULE:FREQ=MONTHLY;COUNT=12']
    }
    events_mock = mock_service.events.return_value
    events_mock.insert.return_value.execute.return_value = mock_event
    
    result = calendar_ops.add_recurring_event(
        summary='Pagamento mensal',
        frequency='monthly',
        count=12,
        start_time='2024-03-01T10:00:00Z',
        end_time='2024-03-01T10:30:00Z'
    )
    
    assert result['status'] == 'confirmed'
    assert 'recurrence' in result
    
    # Verify RRULE for monthly frequency
    events_mock.insert.assert_called_once()
    call_args = events_mock.insert.call_args
    event_data = call_args[1]['body']
    
    assert 'RRULE:FREQ=MONTHLY;COUNT=12' in event_data['recurrence'] 

def test_add_recurring_event_invalid_frequency(calendar_ops, mock_service):
    """Test add_recurring_event with invalid frequency."""
    result = calendar_ops.add_recurring_event(
        summary='Test Event',
        frequency='invalid',  # Invalid frequency
        count=5,
        start_time='2024-03-20T08:00:00Z',
        end_time='2024-03-20T08:30:00Z'
    )
    
    assert result['status'] == 'error'
    assert 'Unsupported frequency: invalid' in result['message']

def test_add_recurring_event_service_error(calendar_ops, mock_service):
    """Test add_recurring_event when service throws an exception."""
    # Mock service to throw an exception
    events_mock = mock_service.events.return_value
    events_mock.insert.return_value.execute.side_effect = Exception("Service error")
    
    result = calendar_ops.add_recurring_event(
        summary='Test Event',
        frequency='daily',
        count=5,
        start_time='2024-03-20T08:00:00Z',
        end_time='2024-03-20T08:30:00Z'
    )
    
    assert result['status'] == 'error'
    assert 'Service error' in result['message'] 