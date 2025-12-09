# Library Limitations & Workarounds

This document outlines what `json_therule0` can and cannot handle, along with practical solutions for each limitation.

## Hard Limitations (Can't Fix Without External Dependencies)

### 1. Datetime/Timestamp Parsing

**Problem**: ISO 8601 dates like `"2024-12-10T14:30:00Z"` stay as strings, not parsed to datetime objects.

**Why**: No automatic detection of date patterns to keep the library dependency-free.

**Impact**:
- Can't sort by date automatically
- Can't filter by date range
- Stats won't compute date-based calculations

**Workaround - Option A: Manual Parsing**
```python
from datetime import datetime
from json_therule0 import read_json

data = read_json('events.json')

# Parse dates manually after loading
records = data.data()
for record in records:
    if 'timestamp' in record:
        record['timestamp'] = datetime.fromisoformat(
            record['timestamp'].replace('Z', '+00:00')
        )
```

**Workaround - Option B: Use pandas for Date Handling**
```python
import pandas as pd
from json_therule0 import read_json

data = read_json('events.json')
df = pd.DataFrame(data.data())
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Now you can do date operations
df_sorted = df.sort_values('timestamp')
```

**Workaround - Option C: Extract Date Components**
```python
# Keep dates as strings but extract year/month/day for analysis
records = data.data()
for record in records:
    if 'timestamp' in record:
        date_str = record['timestamp']
        record['date'] = date_str.split('T')[0]  # Extract date part
        record['year'] = date_str[:4]
        record['month'] = date_str[5:7]
```

---

### 2. Binary/Blob Data

**Problem**: JSON spec doesn't support binary data (images, files, etc.).

**Why**: JSON is text-based; binary data needs encoding.

**Impact**:
- Can't embed images or files directly
- Will error if attempting to load JSON with binary data

**Workaround: Use Base64 Encoding**
```python
import base64
import json
from json_therule0 import read_json

# To create JSON with binary data:
with open('image.png', 'rb') as f:
    image_data = base64.b64encode(f.read()).decode('utf-8')

data = [
    {"id": 1, "image": image_data}
]

with open('data_with_image.json', 'w') as f:
    json.dump(data, f)

# To read it back:
loaded_data = read_json('data_with_image.json')
record = loaded_data.data()[0]
image_bytes = base64.b64decode(record['image'])

with open('decoded_image.png', 'wb') as f:
    f.write(image_bytes)
```

**Better Workaround: Store References Instead**
```python
# Don't embed binary in JSON, just reference it:
data = [
    {"id": 1, "name": "Alice", "photo_path": "photos/alice.jpg"},
    {"id": 2, "name": "Bob", "photo_path": "photos/bob.jpg"}
]

# Then load photos separately when needed
import os
for record in data:
    if os.path.exists(record['photo_path']):
        with open(record['photo_path'], 'rb') as f:
            photo = f.read()
```

---

### 3. Circular References

**Problem**: Objects that reference themselves cause infinite loops.

**Why**: JSON spec doesn't allow circular references; Python's JSON encoder will error.

**Impact**:
- Will crash with `ValueError: Circular reference detected`
- Can't save objects that reference themselves

**Workaround: Flatten the Structure**
```python
# BAD: Circular reference
# user['friends'] = [user]  # User is their own friend!

# GOOD: Use IDs instead
users_data = [
    {"id": 1, "name": "Alice", "friend_ids": [2, 3]},
    {"id": 2, "name": "Bob", "friend_ids": [1]},
    {"id": 3, "name": "Charlie", "friend_ids": [1, 2]}
]

# If you need to rebuild the circular structure in memory:
users_by_id = {u['id']: u for u in users_data}
for user in users_data:
    user['friends'] = [users_by_id[fid] for fid in user['friend_ids']]
    # Now you have circular refs in memory (don't save back to JSON!)
```

---

### 4. NaN and Infinity Values

**Problem**: Scientific/mathematical data with `NaN` or `Infinity` can't be represented.

**Why**: JSON spec requires `null`, not `NaN`/`Infinity`.

**Impact**:
- Will get `ValueError: Out of range float values are not JSON serializable`
- Statistics with missing data won't preserve special float values

**Workaround: Convert to Null or String**
```python
import math
import json

# BAD: This will fail
data = [{"value": float('nan')}, {"value": float('inf')}]
# json.dumps(data)  # ERROR!

# GOOD: Convert to null or string
def sanitize_floats(obj):
    if isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return None  # Convert to null
    elif isinstance(obj, dict):
        return {k: sanitize_floats(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [sanitize_floats(item) for item in obj]
    return obj

data = [{"value": float('nan')}, {"value": float('inf')}]
data = sanitize_floats(data)
# Now safe to save!

# Or preserve as string for documentation
def sanitize_floats_preserve(obj):
    if isinstance(obj, float):
        if math.isnan(obj):
            return "NaN"
        elif math.isinf(obj):
            return "Infinity" if obj > 0 else "-Infinity"
    elif isinstance(obj, dict):
        return {k: sanitize_floats_preserve(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [sanitize_floats_preserve(item) for item in obj]
    return obj
```

---

### 5. Comments in JSON

**Problem**: JSON with comments like `// comment` or `/* block */` won't parse.

**Why**: Standard JSON spec doesn't include comments.

**Impact**:
- Will get `MalformedJSONError`
- Can't use JSON files with documentation comments

**Workaround - Option A: Use JSONC Pre-processor**
```python
import json
import re

def remove_comments(json_str):
    """Remove single-line and block comments from JSON."""
    # Remove single-line comments
    json_str = re.sub(r'//.*?$', '', json_str, flags=re.MULTILINE)
    # Remove block comments
    json_str = re.sub(r'/\*.*?\*/', '', json_str, flags=re.DOTALL)
    return json_str

# Read JSONC file
with open('data.jsonc', 'r') as f:
    content = f.read()

# Remove comments
clean_json = remove_comments(content)
data = json.loads(clean_json)
```

**Workaround - Option B: Use jsonc-parser Library**
```python
# pip install jsonc-parser
from jsonc_parser.parser import parse_file

data = parse_file('data.jsonc')
```

**Workaround - Option C: Convert to Standard JSON**
```python
# Just remove comments before processing
with open('data.jsonc', 'r') as f:
    lines = f.readlines()

# Filter out comment lines
clean_lines = [line for line in lines if not line.strip().startswith('//')]
clean_json_str = ''.join(clean_lines)

# Save as standard JSON
with open('data_clean.json', 'w') as f:
    f.write(clean_json_str)
```

---

### 6. Duplicate Keys

**Problem**: Same key appearing multiple times has undefined behavior (last value wins).

**Why**: JSON spec is ambiguous; Python dict keeps only last value.

**Impact**:
- Silent data loss - no warning about overwritten values
- Can't track that a key appeared multiple times

**Workaround: Validate Before Loading**
```python
import json

def check_duplicate_keys(filepath):
    """Check for duplicate keys in JSON file."""
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Simple regex check
    import re
    # This is a basic check - not foolproof
    lines = content.split('\n')
    keys_seen = {}
    
    for line_num, line in enumerate(lines, 1):
        match = re.search(r'"([^"]+)"\s*:', line)
        if match:
            key = match.group(1)
            if key in keys_seen:
                print(f"Warning: Duplicate key '{key}' at line {line_num} (first seen at {keys_seen[key]})")
            else:
                keys_seen[key] = line_num

check_duplicate_keys('data.json')

# Then load as normal
from json_therule0 import read_json
data = read_json('data.json')
```

**Workaround: Use Custom JSON Decoder**
```python
import json

class DuplicateKeyChecker(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(object_pairs_hook=self.pairs_hook, *args, **kwargs)
    
    def pairs_hook(self, pairs):
        seen = set()
        for key, value in pairs:
            if key in seen:
                raise ValueError(f"Duplicate key found: {key}")
            seen.add(key)
        return dict(pairs)

with open('data.json', 'r') as f:
    try:
        data = json.load(f, cls=DuplicateKeyChecker)
    except ValueError as e:
        print(f"Error: {e}")
```

---

## Performance Limitations

### 1. Memory Usage

**Problem**: Entire file loaded into memory (no streaming).

**When It Breaks**:
- Files > 1GB on systems with limited RAM
- Loading 1M+ record JSON causes slowdowns

**Workaround - Option A: Split Large Files**
```python
import json

def split_json_file(input_file, chunk_size=10000):
    """Split large JSON file into smaller chunks."""
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i+chunk_size]
        chunk_file = f"chunk_{i//chunk_size}.json"
        with open(chunk_file, 'w') as f:
            json.dump(chunk, f)
    
    print(f"Split into {(len(data) + chunk_size - 1) // chunk_size} files")

# Use chunks
from json_therule0 import read_json

all_data = []
for i in range(100):  # Process 100 chunks
    chunk_file = f"chunk_{i}.json"
    try:
        data = read_json(chunk_file)
        all_data.extend(data.data())
    except FileNotFoundError:
        break

print(f"Loaded {len(all_data)} records total")
```

**Workaround - Option B: Use pandas with chunking**
```python
import pandas as pd

# For very large files, use pandas with read_json in chunks
chunks = []
for chunk in pd.read_json('large_file.json', lines=True, chunksize=10000):
    # Process chunk
    chunks.append(chunk)

full_df = pd.concat(chunks)
```

**Workaround - Option C: Use ijson for Streaming**
```python
# pip install ijson
import ijson

with open('large_file.json', 'rb') as f:
    for item in ijson.items(f, 'item'):
        # Process item one at a time
        print(item)
        # Don't store all in memory
```

---

### 2. Deep Recursion Limits

**Problem**: Very deeply nested structures (>1000 levels) hit Python's recursion limit.

**When It Breaks**:
- Nesting exceeds ~1000 levels
- `flatten_dict()` hits `RecursionError`
- Complex COCO-like formats with extreme nesting

**Workaround: Convert to Iterative Flattening**
```python
def flatten_dict_iterative(d, parent_key='', sep='_', max_depth=50):
    """Iteratively flatten dict to avoid recursion limits."""
    items = []
    stack = [(d, parent_key, 0)]
    
    while stack:
        current_dict, current_key, depth = stack.pop()
        
        if depth > max_depth:
            items.append((current_key, str(current_dict)))
            continue
        
        if isinstance(current_dict, dict):
            for k, v in current_dict.items():
                new_key = f"{current_key}{sep}{k}" if current_key else k
                if isinstance(v, dict):
                    stack.append((v, new_key, depth + 1))
                else:
                    items.append((new_key, v))
        else:
            items.append((current_key, current_dict))
    
    return dict(items)

# Use instead of normalizer
deeply_nested = {"a": {"b": {"c": {"d": "value"}}}}
flattened = flatten_dict_iterative(deeply_nested)
print(flattened)  # {'a_b_c_d': 'value'}
```

---

### 3. No Streaming / JSONL Not Supported

**Problem**: Can't process newline-delimited JSON (JSONL) line-by-line.

**When It Breaks**:
- Working with log files (each line is JSON)
- Real-time data feeds
- Processing files larger than memory

**Workaround: Process JSONL Manually**
```python
import json

def read_jsonl(filepath):
    """Read newline-delimited JSON file."""
    data = []
    with open(filepath, 'r') as f:
        for line in f:
            if line.strip():
                data.append(json.loads(line))
    return data

# Then load with library
from json_therule0 import Analyzer

jsonl_data = read_jsonl('data.jsonl')
analyzer = Analyzer(jsonl_data)
print(analyzer.stats())
```

**Better Workaround: Process Line-by-Line**
```python
import json

def process_jsonl_streaming(filepath, process_fn):
    """Process JSONL file line by line without loading all."""
    with open(filepath, 'r') as f:
        for line_num, line in enumerate(f, 1):
            if line.strip():
                record = json.loads(line)
                process_fn(record, line_num)

# Example: Count records by type
type_counts = {}

def count_types(record, line_num):
    type_val = record.get('type', 'unknown')
    type_counts[type_val] = type_counts.get(type_val, 0) + 1

process_jsonl_streaming('data.jsonl', count_types)
print(f"Type counts: {type_counts}")
```

---

## Feature Limitations (Intentional Simplicity)

### 1. No Datetime Type Detection

**Limitation**: Datetime strings not auto-detected or converted.

**Workaround**: See [Datetime/Timestamp Parsing](#1-datetimetimestamp-parsing) section above.

---

### 2. No Groupby/Aggregation

**Limitation**: Can't do `.groupby('city').sum()` style operations.

**Workaround - Option A: Manual Grouping**
```python
from json_therule0 import read_json
from collections import defaultdict

data = read_json('sales.json')
records = data.data()

# Manual groupby
by_city = defaultdict(list)
for record in records:
    city = record.get('city')
    by_city[city].append(record)

# Manual aggregation
for city, city_records in by_city.items():
    total = sum(r.get('amount', 0) for r in city_records)
    print(f"{city}: ${total}")
```

**Workaround - Option B: Use pandas**
```python
import pandas as pd
from json_therule0 import read_json

data = read_json('sales.json')
df = pd.DataFrame(data.data())

# Now pandas groupby works
by_city = df.groupby('city')['amount'].sum()
print(by_city)
```

---

### 3. No Regex/Pattern Filtering

**Limitation**: Only exact value matching, no pattern matching.

**Workaround - Option A: Manual Filtering**
```python
from json_therule0 import read_json
import re

data = read_json('users.json')
records = data.data()

# Filter by pattern
pattern = re.compile(r'^john.*')
filtered = [r for r in records if pattern.match(str(r.get('name', '')))]
print(f"Found {len(filtered)} matches")
```

**Workaround - Option B: Use Processor Directly**
```python
from json_therule0 import Processor

processor = Processor('users.json')
processor.clean()
records = processor.get_cleaned_data()

# Custom filtering
import re
emails_with_gmail = [
    r for r in records 
    if re.search(r'@gmail\.com', r.get('email', ''))
]
```

---

### 4. No Type Validation/Schema Enforcement

**Limitation**: No schema validation - any data structure accepted.

**Workaround: Use pydantic**
```python
# pip install pydantic
from pydantic import BaseModel, ValidationError
from json_therule0 import read_json
from typing import Optional

class User(BaseModel):
    id: int
    name: str
    age: int
    email: Optional[str] = None

data = read_json('users.json')
valid_users = []

for record in data.data():
    try:
        user = User(**record)
        valid_users.append(user)
    except ValidationError as e:
        print(f"Invalid record: {e}")

print(f"Valid users: {len(valid_users)}")
```

---

### 5. No Computed Columns/Transformations

**Limitation**: Can't add derived columns automatically.

**Workaround: Manual Transformation**
```python
from json_therule0 import read_json

data = read_json('sales.json')
records = data.data()

# Add computed columns
for record in records:
    amount = record.get('amount', 0)
    tax_rate = record.get('tax_rate', 0.1)
    record['tax'] = amount * tax_rate
    record['total'] = amount + record['tax']

# Now export with new columns
analyzer = Analyzer(records)
analyzer.to_csv('sales_with_tax.csv')
```

---

## When to Use Alternatives

### Use **pandas** when you need:
- Groupby/aggregation
- Complex data transformations
- Time series operations
- Statistical analysis

### Use **polars** when you need:
- Extreme performance on large files
- Parallel processing
- Low memory usage

### Use **ijson** when you need:
- Streaming large JSON files
- Line-by-line processing
- Memory-efficient parsing

### Use **pydantic** when you need:
- Type validation
- Schema enforcement
- Data parsing and validation

### Use **json_therule0** when you need:
- Quick JSON loading and cleaning
- Simple filtering and selection
- Exploratory data work
- Export to CSV
- Handling unstructured/nested JSON

---

## Summary Table

| Issue | Severity | Workaround Difficulty | Recommendation |
|-------|----------|----------------------|-----------------|
| No datetime parsing | Medium | Easy | Use pandas or manual parsing |
| No binary support | Low | Easy | Use base64 encoding |
| No circular refs | Low | Easy | Use ID references |
| NaN/Infinity | Low | Easy | Convert to null or string |
| Comments in JSON | Low | Easy | Use pre-processor |
| Duplicate keys | Medium | Medium | Validate before loading |
| Memory limits | High | Medium | Use chunking or streaming |
| Deep recursion | Low | Medium | Use iterative flattening |
| No streaming | Medium | Medium | Use ijson or chunking |
| No groupby | Medium | Easy | Use pandas |
| No regex | Low | Easy | Manual filtering |
| No validation | Medium | Easy | Use pydantic |
| No computed columns | Low | Easy | Manual transformation |

---

## Quick Reference: Common Use Cases

### ✅ Works Well
- Loading messy JSON from APIs
- Quick analysis and exploration
- Converting nested JSON to tabular format
- Exporting to CSV
- Filtering and sorting

### ⚠️ Needs Workaround
- Large files (use chunking)
- Datetime operations (use pandas)
- Complex transformations (use pandas)
- Schema validation (use pydantic)

### ❌ Not Supported
- Binary data (use base64)
- Circular references (use IDs)
- Real-time streaming (use ijson)
- Comments in JSON (use pre-processor)

---

## Tip: Exploring Deeply Nested Records

When working with deeply nested data, use the built-in display methods:

```python
from json_therule0 import read_json

data = read_json('deeply_nested.json')

# View full record with all nesting levels
data.display_record(0)

# View record truncated at depth 2 (prevents huge output)
data.display_record(0, max_depth=2)

# Get record as dict for manual inspection
record = data.peek(0)
print(record['api_response']['data'][0])
```

**When to Use Each:**
- `display_record(index)` - See full structure with pretty formatting
- `display_record(index, max_depth)` - Control output size for huge nested data
- `peek(index)` - Get dict for programmatic access to specific fields

