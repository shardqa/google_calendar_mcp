import pytest
from src.core.calendar_ops import CalendarOperations
from unittest.mock import Mock

class TestEnsureTimezone:
    
    def setup_method(self):
        mock_service = Mock()
        self.calendar_ops = CalendarOperations(mock_service)
    
    def test_ensure_timezone_already_has_z_suffix(self):
        """Test that datetime strings ending with Z are not modified."""
        input_time = "2024-03-20T10:00:00Z"
        result = self.calendar_ops._ensure_timezone(input_time)
        assert result == "2024-03-20T10:00:00Z"
    
    def test_ensure_timezone_already_has_plus_offset(self):
        """Test that datetime strings with +XX:XX offset are not modified."""
        input_time = "2024-03-20T10:00:00+03:00"
        result = self.calendar_ops._ensure_timezone(input_time)
        assert result == "2024-03-20T10:00:00+03:00"
    
    def test_ensure_timezone_already_has_minus_offset(self):
        """Test that datetime strings with -XX:XX offset are not modified."""
        input_time = "2024-03-20T10:00:00-05:00"
        result = self.calendar_ops._ensure_timezone(input_time)
        assert result == "2024-03-20T10:00:00-05:00"
    
    def test_ensure_timezone_adds_utc_to_datetime_with_microseconds(self):
        """Test adding UTC timezone to datetime with microseconds."""
        input_time = "2024-03-20T10:00:00.123456"
        result = self.calendar_ops._ensure_timezone(input_time)
        assert result == "2024-03-20T10:00:00.123456+00:00"
    
    def test_ensure_timezone_adds_utc_to_datetime_without_microseconds(self):
        """Test adding UTC timezone to datetime without microseconds."""
        input_time = "2024-03-20T10:00:00"
        result = self.calendar_ops._ensure_timezone(input_time)
        assert result == "2024-03-20T10:00:00.000+00:00"
    
    def test_ensure_timezone_handles_isoformat_output(self):
        """Test handling typical output from datetime.isoformat()."""
        input_time = "2024-03-20T15:30:45.123456"
        result = self.calendar_ops._ensure_timezone(input_time)
        assert result == "2024-03-20T15:30:45.123456+00:00"
    
    def test_ensure_timezone_edge_case_short_offset_plus(self):
        """Test edge case with short positive timezone offset."""
        input_time = "2024-03-20T10:00:00+0100"
        result = self.calendar_ops._ensure_timezone(input_time)
        assert result == "2024-03-20T10:00:00+0100"
    
    def test_ensure_timezone_edge_case_short_offset_minus(self):
        """Test edge case with short negative timezone offset."""
        input_time = "2024-03-20T10:00:00-0300"
        result = self.calendar_ops._ensure_timezone(input_time)
        assert result == "2024-03-20T10:00:00-0300" 