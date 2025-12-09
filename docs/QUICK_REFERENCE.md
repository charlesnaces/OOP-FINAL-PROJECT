# Quick Reference - 3 Core Modules

## **Structure**
```
Processor (Load + Clean)
    ↓
Analyzer (Analyze)
    ↓
JSONFile (Smart wrapper with exception handling)

Normalizer (Optional preprocessor for unstructured JSON)
```

## **When to Use What**

### **Users (99% of cases)**
Use `read_json()` - it handles everything automatically

```python
from json_therule0 import read_json
data = read_json('file.json')
```

### **If Processor Fails**
JSONFile automatically tries Normalizer

```
read_json('coco_format.json')
→ Processor fails (InvalidRootError)
→ Normalizer converts it
→ Processor cleans it
→ Analyzer analyzes it
```

### **Advanced Users**
Direct module imports

```python
from json_therule0 import Processor, Analyzer, Normalizer

processor = Processor('data.json')
analyzer = Analyzer(processor.get_cleaned_data())

# Or for unstructured
normalizer = Normalizer('data.json')
```

---

## **Exception Handling**

| Exception | Cause | Solution |
|-----------|-------|----------|
| FileNotFoundError | File missing | Check file path |
| MalformedJSONError | Invalid JSON | Check JSON syntax |
| InvalidRootError | Not a list | Use Normalizer |

JSONFile handles InvalidRootError automatically by using Normalizer.

---

## **File Size**
- Processor: 225 lines (load + clean)
- Analyzer: 174 lines (analysis)
- Normalizer: 244 lines (unstructured handling)
- JSONFile: ~165 lines (orchestration)

Total: ~800 lines for complete functionality

---

## **API at a Glance**

```python
data = read_json('file.json')

# Display
data.head(n=5)
data.tail(n=5)
data.info()
data.summary()

# Inspect
rows, cols = data.shape()
cols = data.columns()
all_data = data.data()

# Analyze
stats_dict = data.stats()

# Filter
filtered = data.filter('column_name', value)

# Export
data.to_csv('output.csv')
data.to_json('output.json')
```

---

## **Implicit OOP**

- **Encapsulation**: Private attributes `__data`, `__cleaned_data` hide internals
- **Composition**: JSONFile orchestrates Processor, Normalizer, Analyzer
- **Method Chaining**: `processor.trim().drop_null().drop_duplicates()`
- **Single Responsibility**: Each class does one thing well
- **No Inheritance**: Keeps things simple and composition-based

No explicit "look at me, I'm using OOP!" - it's just good design.
