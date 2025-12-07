import pytest
from json_therule0.reader import JSONReader


@pytest.fixture
def sample_data():
    """Provides sample JSON data for tests."""
    return [
        {"id": 1, "name": "Alice", "age": 30},
        {"id": 2, "name": "Bob", "age": 25},
        {"id": 3, "name": "Charlie", "age": 35},
    ]


def test_reader_gets_all_records(sample_data):
    """Tests that JSONReader retrieves all records."""
    reader = JSONReader(sample_data)
    records = reader.get_all()

    assert len(records) == 3
    assert records == sample_data


def test_reader_gets_first_record(sample_data):
    """Tests that JSONReader retrieves the first record."""
    reader = JSONReader(sample_data)
    first = reader.get_first()

    assert first == sample_data[0]
    assert first["name"] == "Alice"


def test_reader_gets_last_record(sample_data):
    """Tests that JSONReader retrieves the last record."""
    reader = JSONReader(sample_data)
    last = reader.get_last()

    assert last == sample_data[-1]
    assert last["name"] == "Charlie"


def test_reader_filters_records(sample_data):
    """Tests that JSONReader filters records by condition."""
    reader = JSONReader(sample_data)
    filtered = reader.filter(lambda record: record["age"] > 25)

    assert len(filtered) == 2
    assert all(r["age"] > 25 for r in filtered)
