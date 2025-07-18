import os
import json
import tempfile
import importlib
import pytest


def test_register_and_get(monkeypatch):
    with tempfile.TemporaryDirectory() as tmp:
        fake_path = os.path.join(tmp, 'ics.json')
        monkeypatch.setattr('src.core.ics_registry._REGISTRY_PATH', fake_path, raising=False)
        reg = importlib.import_module('src.core.ics_registry')
        reg.register('work', 'http://example.com/a.ics')
        assert reg.get('work') == 'http://example.com/a.ics'
        data_on_disk = json.load(open(fake_path))
        assert data_on_disk == {'work': 'http://example.com/a.ics'}
        assert reg.list_all() == {'work': 'http://example.com/a.ics'}


def test_load_invalid_json(monkeypatch, tmp_path):
    bad = tmp_path / 'bad.json'
    bad.write_text('{invalid')
    # Import the module and then patch its path to point to invalid JSON
    registry = importlib.import_module('src.core.ics_registry')
    monkeypatch.setattr(registry, '_REGISTRY_PATH', str(bad), raising=False)
    assert registry.list_all() == {}


def test_list_all_no_file(monkeypatch, tmp_path):
    missing = tmp_path / 'none.json'
    registry = importlib.import_module('src.core.ics_registry')
    monkeypatch.setattr(registry, '_REGISTRY_PATH', str(missing), raising=False)
    assert registry.list_all() == {}


def test_register_invalid(monkeypatch, tmp_path):
    fake = tmp_path / 'f.json'
    reg = importlib.import_module('src.core.ics_registry')
    monkeypatch.setattr(reg, '_REGISTRY_PATH', str(fake), raising=False)
    with pytest.raises(ValueError):
        reg.register('', '') 