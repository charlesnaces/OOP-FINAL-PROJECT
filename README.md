# json_therule0

A beginner-friendly Python library that teaches you **Object-Oriented Programming (OOP)** while solving a real problem: **loading, cleaning, and analyzing JSON data**.

## Why Learn This?

JSON files are everywhere (APIs, databases, config files), but they're often messy:
- Extra whitespace
- Missing values (nulls)
- Duplicate records
- Wrong data types

**json_therule0** shows you how to fix these problems using OOP principles like classes, inheritance, and encapsulation.

## Installation

```bash
pip install json-therule0
```

Or clone for development:

```bash
git clone https://github.com/charlesnaces/OOP-FINAL-PROJECT
cd json_therule0
pip install -e .
```

## Quick Start (3 Simple Steps)

```python
from json_therule0 import JSONCleaner, AdvancedJSONReader

# Step 1: Clean your data
cleaner = JSONCleaner('messy_data.json')
cleaned_data = (cleaner
    .trim_whitespace()      # Remove extra spaces
    .remove_null_values()   # Remove empty values
    .remove_duplicates()    # Keep only unique records
    .get_cleaned_data())    # Get the result

# Step 2: Analyze it
reader = AdvancedJSONReader(cleaned_data)

# Step 3: See results
print(reader.summary_stats())       # Statistics for each column
reader.export_to_csv('clean.csv')   # Save as CSV
```

## Running the Demo

```bash
python main.py
```

## What's Inside?

```
json_therule0/
├── __init__.py              # Main entry point (import from here)
├── loader.py                # JSONLoader - reads JSON files
├── cleaner.py               # JSONCleaner - cleans the data
├── reader.py                # JSONReader - analyzes data
├── advanced.py              # AdvancedJSONReader - advanced analysis
└── exceptions.py            # Custom error messages

tests/                       # Unit tests showing how to use each class
data/sample_data.json        # Example JSON file (messy data)
main.py                      # Complete workflow example
```

## OOP Principles

This project is implemented using standard Object-Oriented Programming (OOP) design patterns (encapsulation, inheritance, composition and single-responsibility). Those design decisions are reflected directly in the package code — see the classes in `json_therule0/` and `API_REFERENCE.md` for usage examples and documentation.

## Testing

```bash
pytest
```

All tests pass (5/5 ✅).

## License

MIT License - see LICENSE file for details.