from unittest.mock import MagicMock

from src.core.scheduling_engine import SchedulingEngine


def test_calculate_duration_wrapper():
    engine = SchedulingEngine(MagicMock(), MagicMock())
    result = engine._calculate_duration('2024-03-22T09:00:00Z', '2024-03-22T10:00:00Z')
    assert result == 60 