# json_therule0

A library for loading, cleaning, and reading JSON data.

## Getting Started

This library provides a set of tools to clean and analyze JSON files.

### Directory Structure

- `json_therule0/`: The main package source code.
- `data/`: Contains sample data.
- `examples/`: Contains example usage scripts.
- `tests/`: Contains tests for the library.

### Usage

The main script `main.py` demonstrates the library's workflow. It takes a JSON file as input, cleans it, and provides a summary.

To run the main script with the default sample data:

```bash
python main.py
```

You can also provide a path to a different JSON file:

```bash
python main.py /path/to/your/data.json
```

Here's a programmatic example of how to use the library, based on `examples/basic_usage.py`:

```python
from json_therule0 import JSONCleaner, JSONReader

# 1. Initialize the cleaner, which automatically loads the data
filepath = 'data/sample_data.json'
cleaner = JSONCleaner(filepath)

# 2. Chain cleaning operations
cleaned_data = (
    cleaner
    .trim_whitespace()
    .remove_null_values()
    .convert_type('price', float)
    .remove_duplicates()
    .get_cleaned_data()
)

# 3. Pass the cleaned data to the reader for analysis
reader = JSONReader(cleaned_data)

print(f"Shape of the data (rows, columns): {reader.shape()}")
print(f"Columns: {reader.get_columns()}")
print("\nSummary Statistics:")
print(reader.summary_stats())
```