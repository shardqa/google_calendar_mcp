import pytest
from unittest.mock import patch, MagicMock
import subprocess
import sys
import os
import runpy

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