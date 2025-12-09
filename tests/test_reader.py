import pytest
from json_therule0.analyzer import Analyzer


@pytest.fixture
def sample_data():
    """Provides sample JSON data for tests."""
    return [
        {"id": 1, "name": "Alice", "age": 30},
        {"id": 2, "name": "Bob", "age": 25},
        {"id": 3, "name": "Charlie", "age": 35},
    ]


def test_reader_gets_all_records(sample_data):
    """Tests that Analyzer retrieves all records."""
    analyzer = Analyzer(sample_data)
    records = analyzer.get_all()

    assert len(records) == 3
    assert records == sample_data


def test_reader_gets_first_record(sample_data):
    """Tests that Analyzer retrieves the first record."""
    analyzer = Analyzer(sample_data)
    first = analyzer.head(1)[0]

    assert first == sample_data[0]
    assert first["name"] == "Alice"




def test_reader_gets_last_record(sample_data):
    """Tests that Analyzer retrieves the last record."""
    analyzer = Analyzer(sample_data)
    last = analyzer.tail(1)[0]

    assert last == sample_data[-1]
    assert last["name"] == "Charlie"


def test_reader_filters_records(sample_data):
    """Tests that Analyzer filters records by value."""
    analyzer = Analyzer(sample_data)
    filtered = analyzer.filter_by_value("name", "Alice")

    assert len(filtered) == 1
    assert filtered[0]["name"] == "Alice"
