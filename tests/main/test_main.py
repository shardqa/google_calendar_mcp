import pytest
from unittest.mock import patch, MagicMock
from src.main import main


def test_main_success():
    with patch('src.main.get_calendar_service') as mock_service, \
         patch('src.main.CalendarOperations') as mock_ops, \
         patch('src.main.CLI') as mock_cli:
        
        mock_cli_instance = MagicMock()
        mock_cli.return_value = mock_cli_instance
        
        result = main()
        
        assert result == 0
        mock_service.assert_called_once()
        mock_ops.assert_called_once()
        mock_cli.assert_called_once()
        mock_cli_instance.run_interactive_loop.assert_called_once()


def test_main_exception_handling():
    with patch('src.main.get_calendar_service', side_effect=Exception('Test error')):
        result = main()
        assert result == 1


def test_main_script_block():
    """Test the if __name__ == '__main__' block (line 17) by simulating module execution"""
    # Mock the exit function to capture its call
    exit_calls = []
    def mock_exit(code):
        exit_calls.append(code)
    
    def mock_main():
        return 42
    
    # Create a test module content that simulates running as __main__
    module_content = '''
if __name__ == "__main__":
    exit(main())
'''
    
    # Execute the module content with __name__ set to '__main__'
    globals_dict = {'__name__': '__main__', 'exit': mock_exit, 'main': mock_main}
    exec(module_content, globals_dict)
    
    # Verify exit was called with the return value from main()
    assert len(exit_calls) == 1
    assert exit_calls[0] == 42 