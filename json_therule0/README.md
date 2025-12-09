# json_therule0

A beginner-friendly Python library that teaches Object-Oriented Programming (OOP) by solving a real problem: loading, cleaning, and analyzing JSON data. json_therule0 provides a compact, OOP-driven pipeline to clean messy JSON (trim whitespace, remove nulls, de-duplicate, correct types) and analyze the result with simple, well-documented classes.

## Project overview

Why this exists
- JSON from APIs, logs, or config files is often messy: extra whitespace, nulls, duplicated records, and incorrect types.
- This project demonstrates how to apply core OOP principles—classes, encapsulation, inheritance, and single-responsibility—to build a reusable data-cleaning and analysis tool.
- It’s both a practical utility for preprocessing JSON and an educational example for learners.

Key features
- JSONLoader: safe JSON loading with helpful errors
- JSONCleaner: chainable cleaning methods (trim whitespace, remove nulls, remove duplicates, coerce types)
- JSONReader / AdvancedJSONReader: basic and advanced analysis (summary statistics, type reports, export to CSV)
- Tests and example data to show usage patterns and encourage learning by reading code

## Why Use This?

json_therule0 serves as a dual-purpose Python library: JSON data, often sourced from APIs and configuration files, is rarely clean. This library provides a structured, OOP-driven approach to automatically handle common issues 

 - Data Cleaning: Eliminating extra whitespace, managing missing values (nulls), and removing duplicate records.
 - Data Integrity: Correcting wrong data types to ensure your analysis is accurate.
 - OOP Learning: It's built using core OOP principles (classes, inheritance, and encapsulation), offering a practical learning experience.
 - Practical Use: Provides an Object-Oriented (OOP) pipeline for automatically cleaning messy JSON data (removing whitespace, duplicates, nulls, and correcting data types) to ensure data integrity for analysis.
 - Educational Use: Acts as a beginner-friendly, real-world example of how to apply core OOP principles (classes, inheritance, encapsulation) to solve common data problems.

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

## Usage

Basic (clean → analyze → export)
```python
from json_therule0 import JSONCleaner, AdvancedJSONReader

# Step 1: Clean your file
cleaner = JSONCleaner('data/sample_data.json')
cleaned_data = (
    cleaner
    .trim_whitespace()      # strip extra spaces from string fields
    .remove_null_values()   # drop or filter out null/missing entries
    .remove_duplicates()    # remove duplicate records
    .coerce_types()         # attempt to correct common type issues
    .get_cleaned_data()     # return cleaned list/dict structure
)

# Step 2: Analyze
reader = AdvancedJSONReader(cleaned_data)
print(reader.summary_stats())        # basic stats per field
print(reader.type_report())          # show inferred vs expected types

# Step 3: Export
reader.export_to_csv('clean.csv')    # save cleaned data to CSV
```

One-liner pipeline (method chaining)
```python
cleaned = JSONCleaner('data/sample_data.json') \
    .trim_whitespace() \
    .remove_null_values() \
    .remove_duplicates() \
    .get_cleaned_data()
```

Programmatic loader usage
```python
from json_therule0 import JSONLoader

loader = JSONLoader('path/to/file.json')
data = loader.load()   # returns Python dict/list or raises descriptive errors
```

Running the demo
```bash
python main.py
```
main.py demonstrates the full workflow with the example dataset.

API reference (short)
- JSONLoader(path: str) -> .load() -> dict|list
- JSONCleaner(source: str | dict | list)
  - .trim_whitespace()
  - .remove_null_values(drop_keys: bool = False)
  - .remove_duplicates(key: Optional[str] = None)
  - .coerce_types(schema: Optional[dict] = None)
  - .get_cleaned_data() -> dict|list
- JSONReader / AdvancedJSONReader(data)
  - .summary_stats()
  - .type_report()
  - .export_to_csv(path: str)

(See inline docstrings for full parameter and return descriptions.)

## Running tests

Run unit tests with pytest:
```bash
pytest
```
All included tests should pass (example suite: 5/5 passing). If tests fail, run with -q and inspect failing tracebacks; open an issue or submit a PR with a failing example if needed.
