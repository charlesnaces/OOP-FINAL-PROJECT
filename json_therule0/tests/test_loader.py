import pytest
import json
from pathlib import Path

from json_therule0.loader import JSONLoader
from json_therule0.exceptions import InvalidJSONError


def test_load_valid_json(tmp_path: Path):
    """Tests that JSONLoader successfully loads a valid JSON file."""
    valid_data = [{"id": 1, "name": "test"}]
    file_path = tmp_path / "valid.json"
    file_path.write_text(json.dumps(valid_data))

    loader = JSONLoader(file_path)
    loaded_data = loader.get_raw_data()

    assert loaded_data == valid_data


def test_load_non_existent_file_raises_error(tmp_path: Path):
    """Tests that JSONLoader raises FileNotFoundError for non-existent file."""
    non_existent_path = tmp_path / "non_existent.json"

    with pytest.raises(FileNotFoundError):
        JSONLoader(non_existent_path)


def test_load_malformed_json_raises_error(tmp_path: Path):
    """Tests that JSONLoader raises InvalidJSONError for malformed JSON."""
    malformed_data = '[{"id": 1, "name": "test"}'
    file_path = tmp_path / "malformed.json"
    file_path.write_text(malformed_data)

    with pytest.raises(InvalidJSONError):
        JSONLoader(file_path)


def test_load_json_with_non_list_root_raises_error(tmp_path: Path):
    """Tests that JSONLoader raises InvalidJSONError if JSON root is not a list."""
    invalid_data = {"error": "not a list"}
    file_path = tmp_path / "invalid_root.json"
    file_path.write_text(json.dumps(invalid_data))

    with pytest.raises(InvalidJSONError):
        JSONLoader(file_path)
