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