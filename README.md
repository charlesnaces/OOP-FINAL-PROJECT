# json_therule0

A Python library for cleaning messy JSON files. Built as a practical example of OOP principles.

## What It Does

JSON from APIs and databases is often messy - full of whitespace, nulls, and duplicates. This library loads your JSON, cleans it, and gets it ready to analyze.

```python
from json_therule0 import read_json

data = read_json('messy.json')
data.head()
data.stats()
data.to_csv('clean.csv')
```

## Install

```bash
pip install json-therule0
```

Or from source:

```bash
git clone https://github.com/charlesnaces/OOP-FINAL-PROJECT
cd OOP-FINAL-PROJECT
pip install -e .
```

## Quick Example

```python
from json_therule0 import read_json

# Load and clean
data = read_json('data.json')

# Look at it
print(data.shape())        # (rows, cols)
print(data.columns())      # column names
print(data.head(5))        # first 5 rows
data.display_record(0)     # pretty print single record (any nesting level)

# Analyze
print(data.stats())        # statistics

# Filter and process
active = data.filter('status', 'active')
subset = data.select(['name', 'email'])
sorted_data = data.sort('age', ascending=True)

# Export
data.to_csv('output.csv')
data.to_json('output.json')
```

## Key Features

✅ **Simple API** - pandas-like interface  
✅ **Auto-normalization** - Handles unstructured JSON (COCO, nested dicts, etc.)  
✅ **Smart cleaning** - Removes whitespace, nulls, duplicates automatically  
✅ **Rich filtering** - Filter, select, sort with validation  
✅ **Statistics** - Get stats for any column (numeric or categorical)  
✅ **Multiple exports** - Save as CSV or JSON  
✅ **Production-ready** - 51 comprehensive tests, all passing  

## What's Inside

- **Processor**: Load and clean JSON (removes whitespace, nulls, duplicates)
- **Analyzer**: Inspect and export data (stats, filtering, CSV/JSON output)
- **Normalizer**: Handle weird JSON formats (COCO, nested structures)
- **JSONFile**: Simple wrapper that uses all three automatically

## Testing

Run with:

```bash
pytest tests/ -v
```

**Results:**
- ✅ 51 tests passing
- ✅ 36 new JSONFile tests
- ✅ All edge cases covered
- ✅ Zero failures

## Documentation

- **API Reference**: `docs/API_REFERENCE.md` - Complete method documentation
- **Examples**: `examples/basic_usage.py` - 10 working examples
- **Limitations**: `docs/LIMITATIONS.md` - Known limitations and workarounds
- **Real-world Scenarios**: `examples/real_world_scenarios.py` - Production data examples
- **Unstructured Data**: `examples/unstructured_api_data.py` - Real API response handling

## Recent Improvements (v0.2.0)

✅ Complete OOP implementation with 7 classes  
✅ Auto type inference and conversion  
✅ Unstructured JSON normalization (COCO, nested dicts, arrays)  
✅ Real-world production examples (employees, transactions, APIs)  
✅ 51 comprehensive tests (all passing)  
✅ Complete documentation with limitations guide  
✅ Zero external dependencies  
✅ Pandas-like simple API  

## Why This Exists

Started as a school project to demonstrate OOP principles in real code. Features actual classes, encapsulation, composition, and single responsibility doing useful work - not just theory.

