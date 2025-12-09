# API Reference

## Basic Usage

```python
from json_therule0 import read_json

# Load and clean your JSON file
data = read_json('data.json')

# Look at first/last few records
data.head(5)
data.tail(5)

# Check dimensions
print(data.shape())      # (rows, columns)
print(data.columns())    # column names

# Get stats
print(data.stats())

# Filter records
filtered = data.filter('name', 'Alice')

# Export
data.to_csv('output.csv')
data.to_json('output.json')
```

## Main Classes

### `JSONFile` - The Entry Point

Use `read_json()` to get a `JSONFile` object. It handles everything automatically:
- Loads the JSON
- Cleans it (removes whitespace, nulls, duplicates)
- Auto-converts types (int/float/bool detection)
- Auto-normalizes unstructured JSON (COCO, nested dicts, arrays)
- Gets it ready to analyze

```python
data = read_json('file.json')
```

### `Processor` - Load & Clean

If you need fine-grained control:

```python
from json_therule0 import Processor

processor = Processor('data.json')
processor.trim()
processor.drop_null()
processor.drop_duplicates()

cleaned = processor.get_cleaned_data()
```

Methods:
- `trim()` - remove leading/trailing whitespace
- `drop_null()` - remove records with None values
- `drop_duplicates()` - remove exact duplicates
- `clean()` - apply all three above
- `get_cleaned_data()` - get the result

### `Analyzer` - Inspect & Export

Analyze cleaned data (read-only):

```python
from json_therule0 import Analyzer

analyzer = Analyzer(cleaned_data)
analyzer.head(10)
analyzer.stats()
analyzer.filter_by_value('status', 'active')
analyzer.to_csv('output.csv')
```

Methods:
- `head(n)` - first n records
- `tail(n)` - last n records
- `shape()` - (rows, columns)
- `columns()` - column names
- `stats()` - statistics per column
- `filter_by_value(col, val)` - filter records
- `to_csv(path)` - save as CSV
- `to_json(path)` - save as JSON

### `JSONFile` - Display Single Records

When working with nested/unstructured data, use these methods:

```python
data = read_json('nested_data.json')

# Display a single record (handles any nesting depth)
data.display_record(0)                    # Full display
data.display_record(0, max_depth=2)       # Limited depth

# Quick access to a record
record = data.peek(0)
print(record['name'])
```

Methods:
- `display_record(index, max_depth)` - Pretty print single record with JSON formatting
- `peek(index)` - Get record as dict for inspection

### `Normalizer` - Handle Unstructured JSON

For messy JSON that doesn't look like a table (like COCO format):

```python
from json_therule0 import Normalizer

normalizer = Normalizer('messy.json')
normalized = normalizer.normalize_auto()
```

Methods:
- `detect_format()` - figure out the structure
- `normalize()` - convert to tabular format
- `normalize_auto()` - auto-detect and normalize
- `display_structure()` - show what it found

## Common Tasks

### Load and clean in one line
```python
data = read_json('file.json')
```

### Look at the data
```python
data.head(10)      # first 10 rows
data.tail(5)       # last 5 rows
data.info()        # formatted summary
data.summary()     # complete summary
```

### Get info about structure
```python
rows, cols = data.shape()
column_names = data.columns()
all_data = data.data()
```

### Analyze
```python
stats = data.stats()
filtered = data.filter('status', 'active')
```

### Export
```python
data.to_csv('output.csv')
data.to_json('output.json')
```

## Exception Handling

If `read_json()` detects unstructured JSON (like COCO format), it'll automatically try to normalize it before cleaning.

If something goes wrong:
- `FileNotFoundError` - file doesn't exist
- `MalformedJSONError` - broken JSON syntax
- `InvalidRootError` - JSON structure not supported (will try Normalizer)

All errors show helpful messages explaining what went wrong.

---

## Extended Reference

### More Details

For detailed implementation see source files in `src/json_therule0/`

**Classes:**
- `JSONFile` - Main interface (jsonfile.py)
- `Processor` - Loading & cleaning (processor.py)
- `Normalizer` - Unstructured to tabular (normalizer.py)
- `Analyzer` - Analysis & export (analyzer.py)

---

## Version

Current Version: **0.2.0** (Beta)



