def test_remove_event_success(calendar_ops, mock_service):
    event_id = 'test-event-id'
    events_mock = mock_service.events.return_value
    events_mock.delete.return_value.execute.return_value = None
    result = calendar_ops.remove_event(event_id)
    assert result is True
    mock_service.events.assert_called_once()
    events_mock.delete.assert_called_once()
    events_mock.delete.return_value.execute.assert_called_once()

def test_remove_event_failure(calendar_ops, mock_service):
    event_id = 'test-event-id'
    events_mock = mock_service.events.return_value
    events_mock.delete.return_value.execute.side_effect = Exception("Event not found")
    result = calendar_ops.remove_event(event_id)
    assert result is False
    mock_service.events.assert_called_once()
    events_mock.delete.assert_called_once()
    events_mock.delete.return_value.execute.assert_called_once() 