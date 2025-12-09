# json_therule0 - Simplified Pandas-Like API

## One Clear Way to Do Everything

```python
from json_therule0 import read_json

# Load
data = read_json('data.json')

# Display
data.head(5)        # First 5 records
data.tail(5)        # Last 5 records
data.info()         # Formatted info
data.summary()      # Complete summary

# Inspect
data.shape()        # (rows, columns)
data.columns()      # Column names
data.data()         # All records

# Analyze
data.stats()        # Statistics (numeric/categorical)

# Filter
filtered = data.filter('column_name', value)

# Export
data.to_csv('output.csv')
data.to_json('output.json')
```

## Changes Made for Simplicity

### Removed Redundancy
- ❌ REMOVED: `summary_stats()` → ✅ RENAMED TO: `stats()`
- ❌ REMOVED: `get_all()` (kept for backward compatibility, not recommended)
- ❌ REMOVED: `filter()` with callable/predicate
- ❌ REMOVED: `filter_by_value()` returns Analyzer → ✅ NOW returns list
- ❌ REMOVED: `export_to_csv()` → ✅ RENAMED TO: `to_csv()`
- ❌ REMOVED: `describe()` and nested statistics
- ❌ REMOVED: `select()` method (column selection not needed for MVP)

### Simplified API
- `get_columns()` still exists in Analyzer (keep for composition)
- JSONFile has `.columns()` which calls `get_columns()`
- `head()`, `tail()` available on both Analyzer and JSONFile
- `stats()` consistent everywhere
- One way to filter: `data.filter(column, value)` → returns list

### Method Clarity
Each method has ONE clear purpose:
- `.head(n)` - preview first n
- `.tail(n)` - preview last n
- `.stats()` - get statistics
- `.filter(col, val)` - filter records
- `.shape()` - get dimensions
- `.columns()` - get column names
- `.data()` - get all records
- `.to_csv(path)` - export CSV
- `.to_json(path)` - export JSON

## Test Results
✅ All 15 tests passing
✅ Clean, predictable behavior
✅ No confusion about method names
✅ Implicit OOP (encapsulation, composition, method chaining)
