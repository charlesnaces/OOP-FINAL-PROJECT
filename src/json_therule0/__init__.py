# json_therule0/__init__.py

from .processor import Processor
from .analyzer import Analyzer
from .normalizer import Normalizer
from .jsonfile import JSONFile
from .api import read_json
from .exceptions import (
    InvalidJSONError,
    MalformedJSONError,
    InvalidRootError,
    EmptyDataError,
    UnsupportedFormatError,
    DataProcessingError,
    NormalizationError,
    CleaningError,
    FilterError,
    SelectionError,
    SortError,
    AnalysisError,
    ColumnNotFoundError,
    StatisticsError,
    ExportError,
    InvalidExportFormatError,
    FileOperationError,
    FileReadError,
    FileWriteError,
    ValidationError,
    InvalidParameterError,
    DataTypeError,
)

__all__ = [
    # Simple API (recommended)
    "read_json",
    "JSONFile",
    # Core modules
    "Processor",
    "Analyzer",
    "Normalizer",
    # Exceptions
    "InvalidJSONError",
    "MalformedJSONError",
    "InvalidRootError",
    "EmptyDataError",
    "UnsupportedFormatError",
    "DataProcessingError",
    "NormalizationError",
    "CleaningError",
    "FilterError",
    "SelectionError",
    "SortError",
    "AnalysisError",
    "ColumnNotFoundError",
    "StatisticsError",
    "ExportError",
    "InvalidExportFormatError",
    "FileOperationError",
    "FileReadError",
    "FileWriteError",
    "ValidationError",
    "InvalidParameterError",
    "DataTypeError",
]

# Package version
__version__ = "0.2.0"

# Export version as well
__all__.append("__version__")

# Package docstring
__doc__ = """json_therule0: Simple JSON handler for structured and unstructured data.

A lightweight, zero-dependency library for loading, normalizing, and analyzing JSON files.

Quick Start:
    >>> from json_therule0 import read_json
    >>> data = read_json('data.json')
    >>> data.head(5)
    >>> data.stats()
    >>> data.to_csv('output.csv')

Features:
    - Auto-normalization of unstructured JSON (COCO, nested dicts, etc.)
    - Type inference and conversion for mixed-type columns
    - Pandas-like API (head, tail, filter, sort, select)
    - Clean messy data (whitespace, nulls, duplicates)
    - Export to CSV and JSON

Documentation:
    - API Reference: docs/API_REFERENCE.md
    - Examples: examples/
    - Limitations: docs/LIMITATIONS.md
"""
