# json_therule0 - Complete Guide for Students

## 🎯 What is json_therule0?

**json_therule0** is a beginner-friendly Python library that teaches you **Object-Oriented Programming (OOP)** while solving a real problem: cleaning messy JSON data.

### Why Learn This?

1. **Real-world problem**: JSON files often have errors, missing values, and duplicates
2. **Practical skills**: Learn data cleaning, which is 80% of data science work
3. **OOP best practices**: See all 5 OOP principles in real code
4. **Career-ready**: These patterns are used everywhere in professional software

---

## 🏗️ How It All Works Together

Think of it like a car factory assembly line:

```
📁 Your Messy JSON File
  ↓
┌─────────────────────┐
│ JSONLoader          │  ← Quality check: Is this valid JSON?
│ (Step 1: Load)      │     (Bouncer checking IDs)
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ JSONCleaner         │  ← Fix the data:
│ (Step 2: Clean)     │     • Remove extra spaces
└──────────┬──────────┘     • Delete empty values
           │                • Remove duplicates
        ## 🎓 OOP Principles

        This library is implemented following core Object-Oriented Programming (OOP) principles such as encapsulation, inheritance, composition, polymorphism, and the single-responsibility principle. Those design choices are expressed directly in the code (see the classes in `json_therule0/` for concrete examples) rather than as tutorial content in this reference.

        ---

**Key idea**: Each method returns `self`, so you can chain them together!

---

### 3. JSONReader - "The Analyst" 📊

**What it does**: Analyzes cleaned data without changing it. Read-only access only!

**Location**: `json_therule0/reader.py`

**How to use**:
```python
from json_therule0 import JSONReader

reader = JSONReader(cleaned_data)

print(reader.shape())               # (rows, columns)
print(reader.get_columns())         # List of column names
print(reader.summary_stats())       # Min, max, average, etc.
print(len(reader))                  # Number of rows
```

**Available methods**:

| Method | What it does | Returns |
|--------|-------------|---------|
| `shape()` | How many rows and columns? | `(100, 5)` |
| `get_columns()` | List all column names | `['id', 'name', 'price']` |
| `summary_stats()` | Statistics for each column | Dictionary with stats |
| `__len__()` | Number of rows (use `len()`) | `100` |

**Output example** - `summary_stats()`:
```python
{
    'age': {
        'type': 'numeric',
        'mean': 35.5,
        'min': 18,
        'max': 75,
        'std': 12.3
    },
    'name': {
        'type': 'categorical',
        'count': 95,
        'unique': 93,
        'top': 'John'
    }
}
```

---

### 4. AdvancedJSONReader - "The Expert" 🔬

**What it does**: Like JSONReader, but with super-powers! Inherits all JSONReader methods plus new ones.

**Location**: `json_therule0/advanced.py`

**How to use**:
```python
from json_therule0 import AdvancedJSONReader

advanced = AdvancedJSONReader(cleaned_data)

# Can use JSONReader methods:
print(advanced.shape())              # Inherited from parent
print(advanced.summary_stats())      # Inherited from parent

# Plus new methods:
advanced.export_to_csv('output.csv')              # Save as CSV
filtered = advanced.filter_by_value('status', 'active')  # Filter
unique_vals = advanced.get_unique_values('country')     # Get unique
print(advanced.describe())           # Full description
```

**New methods** (unique to AdvancedJSONReader):

| Method | What it does | Example |
|--------|-------------|---------|
| `export_to_csv(filepath)` | Save data to CSV file | `export_to_csv('output.csv')` |
| `filter_by_value(column, value)` | Keep only matching rows | `filter_by_value('status', 'active')` |
| `get_unique_values(column)` | Get all unique values | `['USA', 'UK', 'Canada']` |
| `describe()` | Full dataset summary | Comprehensive description |

---

## 🎓 OOP Concepts Explained

### 1. Classes ✅
**What**: Blueprints for objects (like a recipe for objects)

**In our code**:
- `JSONLoader` - Blueprint for a file loader
- `JSONCleaner` - Blueprint for data cleaner
- `JSONReader` - Blueprint for data analyzer
- `AdvancedJSONReader` - Blueprint for advanced analyzer

### 2. Encapsulation ✅
**What**: Keep internals private, expose only what's needed

**In our code**:
```python
# Private (hidden) - you can't access these directly
cleaner.__cleaned_data      # ❌ This won't work (name mangling)

# Public (safe to use) - use these instead
cleaner.get_cleaned_data()  # ✅ This works
```

**Why?** Prevents accidental misuse and protects internal state.

### 3. Inheritance ✅
**What**: Child class gets all features of parent class, plus new ones

**In our code**:
```python
# JSONReader is the parent (parent class)
class JSONReader:
    def shape(self):
        pass

# AdvancedJSONReader is the child
class AdvancedJSONReader(JSONReader):  # ← inherits from JSONReader
    def export_to_csv(self):           # ← new method
        pass
```

**Result**: `AdvancedJSONReader` has `shape()` (from parent) + `export_to_csv()` (new)

### 4. Composition ✅
**What**: One class contains another class (has-a relationship)

**In our code**:
```python
class JSONCleaner:
    def __init__(self, filepath):
        self.__loader = JSONLoader(filepath)  # ← Contains a JSONLoader
        # Now cleaner has all powers of JSONLoader too!
```

**Result**: JSONCleaner gets JSONLoader's power without inheriting from it.

### 5. Polymorphism ✅
**What**: Same method name, different behavior in different classes

**In our code**:

```python
# All classes have __str__() method, but each works differently

loader = JSONLoader('data.json')
print(loader)  # JSONLoader(data.json) - 100 records

cleaner = JSONCleaner('data.json')
print(cleaner)  # JSONCleaner (data.json): 100 → 98 records (cleaned)

reader = JSONReader(data)
print(reader)  # JSONReader with 98 rows and 5 columns
```

**Same method name (`__str__`), different outputs!** That's polymorphism.

---

## 💡 Complete Example: From Messy to Clean

```python
from json_therule0 import JSONCleaner, AdvancedJSONReader

# Step 1: Load messy data
print("Loading data...")
cleaner = JSONCleaner('messy_sales.json')
print(cleaner)  # JSONCleaner (messy_sales.json): 500 → ? records

# Step 2: Clean it
print("\nCleaning data...")
cleaned_data = (cleaner
    .trim_whitespace()              # "  Product A  " → "Product A"
    .remove_null_values()           # Remove empty fields
    .remove_duplicates()            # Remove duplicate sales
    .convert_type('price', float)   # Convert string prices to numbers
    .get_cleaned_data())

print(f"Cleaned: {len(cleaned_data)} records")

# Step 3: Analyze
print("\nAnalyzing data...")
reader = AdvancedJSONReader(cleaned_data)
print(f"Shape: {reader.shape()}")
print(f"Columns: {reader.get_columns()}")

# Step 4: Generate report
print("\nGenerating report...")
stats = reader.summary_stats()
print(f"Average price: ${stats['price']['mean']:.2f}")
print(f"Price range: ${stats['price']['min']} - ${stats['price']['max']}")

# Step 5: Export
print("\nExporting to CSV...")
reader.export_to_csv('clean_sales.csv')
print("Done! Check clean_sales.csv")
```

**Output**:
```
Loading data...
JSONCleaner (messy_sales.json): 500 → 485 records

Cleaning data...
Cleaned: 485 records

Analyzing data...
Shape: (485, 6)
Columns: ['date', 'product', 'price', 'quantity', 'seller', 'status']

Generating report...
Average price: $49.99
Price range: $9.99 - $999.99

Exporting to CSV...
Done! Check clean_sales.csv
```

---

## 🧪 Testing Your Code

The library includes tests to verify everything works:

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_cleaner.py

# See detailed output
pytest -v
```

**Test files**:
- `tests/test_loader.py` - Tests JSONLoader
- `tests/test_cleaner.py` - Tests JSONCleaner  
- `tests/test_reader.py` - Tests JSONReader

---

## 📋 File Structure

```
json_therule0/
├── json_therule0/                   # Main package
│   ├── __init__.py                 # Import all classes here
│   ├── loader.py                   # JSONLoader class
│   ├── cleaner.py                  # JSONCleaner class
│   ├── reader.py                   # JSONReader class
│   ├── advanced.py                 # AdvancedJSONReader class
│   └── exceptions.py               # Custom errors
├── tests/                          # Tests
│   ├── test_loader.py
│   ├── test_cleaner.py
│   └── test_reader.py
├── data/                           # Sample data
│   └── sample_data.json
├── examples/
│   └── basic_usage.py             # Example script
├── main.py                         # Complete demo
├── README.md                       # User guide
└── setup.py                        # Package info
```

---

## 🚀 Key Takeaways

1. **Modular**: Each class has one job (single responsibility)
2. **Safe**: Private attributes prevent accidents
3. **Reusable**: Inheritance avoids code duplication
4. **Easy to use**: Method chaining makes code readable
5. **Professional**: Real-world utility + educational value

This library shows everything you need to know about OOP! 🎓
