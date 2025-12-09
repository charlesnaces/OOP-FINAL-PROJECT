# Release Notes - v0.2.0

**Release Date**: December 10, 2025  
**Status**: Beta (Production Ready)

## Summary

`json_therule0` is now feature-complete as a lightweight, zero-dependency JSON handler for both structured and unstructured data. This release reflects the maturity of the codebase and real-world usability.

## What's New in v0.2.0

### Core Features
- ✅ **7 OOP Classes** - Clean separation of concerns (Processor, Analyzer, Normalizer, JSONFile, TypeConverter, exceptions, API)
- ✅ **Auto Type Conversion** - Detects and converts mixed-type columns (int/float/bool/str/numeric)
- ✅ **Unstructured JSON Support** - Auto-normalization of COCO format, nested dicts, nested lists, and arrays
- ✅ **Pandas-like API** - Familiar methods: head, tail, filter, sort, select, stats, info, summary
- ✅ **Type Preservation** - Complex types (dicts, lists) preserved during conversion

### Data Processing
- ✅ **Automatic Cleaning** - Whitespace trimming, null removal, duplicate detection
- ✅ **Format Detection** - Automatically detects JSON structure (COCO, nested_dict, nested_list, array, unknown)
- ✅ **Smart Flattening** - Converts deeply nested structures to tabular format with consistent naming

### Testing & Quality
- ✅ **51 Comprehensive Tests** - Full coverage of all features and edge cases
- ✅ **Zero External Dependencies** - Pure Python, no pip requirements
- ✅ **Full Documentation** - API reference, examples, limitations guide
- ✅ **Real-world Examples** - Employee HR, E-commerce transactions, Event management, Social media APIs, User activity logs

### Documentation
- ✅ **API Reference** - Complete method documentation with examples
- ✅ **Limitations Guide** - Honest assessment of what's not supported and practical workarounds
- ✅ **Basic Examples** - 10 working examples covering common tasks
- ✅ **Real-world Scenarios** - Production data examples with analysis
- ✅ **Unstructured Data Examples** - Actual API responses and nested structures

## Breaking Changes

**None** - This is a minor version bump. All v0.1.x code remains compatible.

## Version History

### v0.2.0 (Current)
- Complete OOP implementation
- Type conversion system
- Unstructured JSON support
- Comprehensive documentation

### v0.1.1
- Initial release with core features
- Basic cleaning and analysis
- Pandas-like API

## Known Limitations

See `docs/LIMITATIONS.md` for:
- Hard limitations (datetime parsing, binary data, circular references, etc.)
- Performance limitations (memory, recursion)
- Feature limitations (no logging, no validation, no groupby)
- Practical workarounds for all items

## Supported Python Versions

- Python 3.8+
- Python 3.9
- Python 3.10
- Python 3.11
- Python 3.12

## Testing

All 51 tests pass:
```bash
pytest tests/ -v
```

**Test Results:**
- `test_jsonfile.py`: 36 tests ✅
- `test_cleaner.py`: 2 tests ✅
- `test_loader.py`: 4 tests ✅
- `test_normalizer.py`: 5 tests ✅
- `test_reader.py`: 4 tests ✅

## Next Steps (Future Versions)

**Optional enhancements** (not blocking):
- Logging system for debugging
- Configuration module for customization
- CHANGELOG file for version tracking
- Contributing guide for open source
- CI/CD pipeline (GitHub Actions)
- Type hints improvements

## Migration from v0.1.1

**No migration needed.** Simply update:
```bash
pip install json-therule0==0.2.0
```

All existing code continues to work without changes.

## Quick Start

```python
from json_therule0 import read_json

# Load JSON
data = read_json('data.json')

# Explore
print(data.head())
print(data.info())
print(data.stats())

# Process
filtered = data.filter('status', 'active')
selected = data.select(['name', 'email'])
sorted_data = data.sort('age')

# Export
data.to_csv('output.csv')
data.to_json('output.json')
```

## Documentation

- **README**: Getting started guide
- **API_REFERENCE**: Complete method documentation
- **LIMITATIONS**: Known limitations and workarounds
- **examples/**: Working code examples
- **tests/**: Comprehensive test suite

## Support

- Report issues: GitHub Issues
- Questions: Check examples/ and docs/
- Contribute: Pull requests welcome

## License

MIT License - See LICENSE file

---

**json_therule0** - Making JSON handling simple and straightforward.
