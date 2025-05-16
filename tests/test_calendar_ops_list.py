def test_list_events_empty(calendar_ops, mock_service):
    events_mock = mock_service.events.return_value
    events_mock.list.return_value.execute.return_value = {}
    events = calendar_ops.list_events()
    assert events == []
    mock_service.events.assert_called_once()
    events_mock.list.assert_called_once()
    events_mock.list.return_value.execute.assert_called_once()

def test_list_events_with_results(calendar_ops, mock_service):
    mock_events = {
        'items': [
            {
                'id': '1',
                'summary': 'Test Event',
                'start': {'dateTime': '2024-03-20T10:00:00Z'},
                'end': {'dateTime': '2024-03-20T11:00:00Z'}
            }
        ]
    }
    events_mock = mock_service.events.return_value
    events_mock.list.return_value.execute.return_value = mock_events
    events = calendar_ops.list_events(max_results=5)
    assert len(events) == 1
    assert events[0]['summary'] == 'Test Event'
    mock_service.events.assert_called_once()
    events_mock.list.assert_called_once()
    events_mock.list.return_value.execute.assert_called_once() 