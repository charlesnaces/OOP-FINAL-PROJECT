# json_therule0

A beginner-friendly Python library that teaches Object-Oriented Programming (OOP) by solving real-world problems: loading, cleaning, and analyzing JSON data. Json_therule0 provides a compact, OOP-driven pipeline to clean messy JSON (trim whitespace, remove nulls, de-duplicate, correct types) and analyze the result with simple, well-documented classes.

## Project overview

Why this exists
- JSON from APIs, logs, or config files is often messy, with extra whitespace, nulls, duplicated records, and incorrect types.
- This project explains how to apply core OOP principles—classes, encapsulation, inheritance, and single-responsibility—to build a reusable data-cleaning and analysis tool.
- It’s both a practical utility for preprocessing JSON and an educational example for learners.

Key features
- JSONLoader: safe JSON loading with helpful errors
- JSONCleaner: chainable cleaning methods (trim whitespace, remove nulls, remove duplicates, coerce types)
- JSONReader / AdvancedJSONReader: basic and advanced analysis (summary statistics, type reports, export to CSV)
- Tests and example data to show usage patterns and encourage learning by reading code

## Why Use This?

json_therule0 serves as a dual-purpose Python library: JSON data, often sourced from APIs and configuration files, is rarely clean. This library provides a structured, OOP-driven approach to automatically handle common issues 

 - It eliminates extra whitespace, managing missing values (nulls), and removing duplicate records.
 - Correcting wrong data types to ensure your analysis is accurate.
 - It's built using core OOP principles (classes, inheritance, and encapsulation), offering a practical learning experience.
 - Provides an Object-Oriented (OOP) pipeline for automatically cleaning messy JSON data (removing whitespace, duplicates, nulls, and correcting data types) to ensure data integrity for analysis.
 - It acts as a beginner-friendly, real-world example of how to apply core OOP principles (classes, inheritance, encapsulation) to solve common data problems.

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

