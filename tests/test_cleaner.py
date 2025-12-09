import pytest
import json
from pathlib import Path

from json_therule0.processor import Processor


@pytest.fixture
def sample_json_path(tmp_path: Path) -> Path:
    """Pytest fixture to create a sample JSON file for testing."""
    sample_data = [
        {"id": 1, "name": "  Product A  ", "price": 100},
        {"id": 2, "name": "Product B", "price": 200}
    ]
    file_path = tmp_path / "sample.json"
    file_path.write_text(json.dumps(sample_data))
    return file_path


def test_cleaner_instantiation(sample_json_path: Path):
    """Tests that Processor correctly instantiates."""
    processor = Processor(sample_json_path)
    cleaned_data = processor.get_cleaned_data()

    assert isinstance(cleaned_data, list)
    assert len(cleaned_data) == 2


def test_cleaner_deep_copy(sample_json_path: Path):
    """Tests that Processor creates a deep copy of the data."""
    processor = Processor(sample_json_path)
    cleaned_data = processor.get_cleaned_data()

    # Modify the cleaned data
    cleaned_data[0]["name"] = "MODIFIED"

    # Get the cleaned data again - should be unchanged
    cleaned_data_again = processor.get_cleaned_data()
    assert cleaned_data_again[0]["name"] == "  Product A  "
