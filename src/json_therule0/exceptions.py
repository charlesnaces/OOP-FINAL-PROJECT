# json_therule0/exceptions.py

"""
Custom exceptions for the json_therule0 library.

Exception hierarchy:
    Exception
    ├── InvalidJSONError (base for all JSON-related errors)
    │   ├── MalformedJSONError
    │   ├── InvalidRootError
    │   ├── EmptyDataError
    │   └── UnsupportedFormatError
    ├── DataProcessingError
    │   ├── NormalizationError
    │   ├── CleaningError
    │   └── FilterError
    ├── AnalysisError
    │   ├── ColumnNotFoundError
    │   ├── StatisticsError
    │   └── ExportError
    └── FileOperationError
        ├── FileNotFoundError (builtin)
        ├── FileReadError
        └── FileWriteError
"""


# ============ Base Exceptions ============

class InvalidJSONError(Exception):
    """
    Base exception for errors related to invalid JSON format.
    All JSON structure-related errors inherit from this.
    """
    pass


class DataProcessingError(Exception):
    """
    Base exception for errors during data processing operations.
    Raised when data transformation fails.
    """
    pass


class AnalysisError(Exception):
    """
    Base exception for errors during data analysis operations.
    Raised when analysis or statistics computation fails.
    """
    pass


class FileOperationError(Exception):
    """
    Base exception for file operation errors.
    Raised when file I/O operations fail.
    """
    pass


# ============ JSON Format Errors ============

class MalformedJSONError(InvalidJSONError):
    """
    Exception raised when JSON syntax is invalid.
    Occurs during JSON parsing/decoding.
    """
    pass


class InvalidRootError(InvalidJSONError):
    """
    Exception raised when the JSON root structure is invalid.
    Expected: list of objects at root level
    Got: dict, string, array of non-objects, etc.
    """
    pass


class EmptyDataError(InvalidJSONError):
    """
    Exception raised when JSON file is empty or contains no valid data.
    Occurs with empty arrays [] or after filtering results in no records.
    """
    pass


class UnsupportedFormatError(InvalidJSONError):
    """
    Exception raised when JSON format is not recognized or supported.
    Occurs with unusual/custom JSON structures that cannot be normalized.
    """
    pass


# ============ Data Processing Errors ============

class NormalizationError(DataProcessingError):
    """
    Exception raised when data normalization fails.
    Occurs when converting unstructured JSON to tabular format.
    """
    pass


class CleaningError(DataProcessingError):
    """
    Exception raised when data cleaning operations fail.
    Occurs during whitespace trimming, null removal, or deduplication.
    """
    pass


class FilterError(DataProcessingError):
    """
    Exception raised when filtering operations fail.
    Occurs when column doesn't exist or filter conditions are invalid.
    """
    pass


class SelectionError(DataProcessingError):
    """
    Exception raised when column selection fails.
    Occurs when specified columns don't exist in the data.
    """
    pass


class SortError(DataProcessingError):
    """
    Exception raised when sorting operations fail.
    Occurs when sort column doesn't exist or data types are incompatible.
    """
    pass


# ============ Analysis Errors ============

class ColumnNotFoundError(AnalysisError):
    """
    Exception raised when a specified column is not found in the data.
    Occurs in filter(), select(), sort(), or stats() operations.
    """
    pass


class StatisticsError(AnalysisError):
    """
    Exception raised when statistics computation fails.
    Occurs when calculating mean, std, percentiles, etc.
    """
    pass


class ExportError(AnalysisError):
    """
    Exception raised when exporting data to file fails.
    Occurs during to_csv() or to_json() operations.
    """
    pass


class InvalidExportFormatError(ExportError):
    """
    Exception raised when specified export format is not supported.
    Supported formats: 'csv', 'json'
    """
    pass


# ============ File Operation Errors ============

class FileReadError(FileOperationError):
    """
    Exception raised when reading a file fails.
    Occurs with permission errors or corrupted files.
    """
    pass


class FileWriteError(FileOperationError):
    """
    Exception raised when writing to a file fails.
    Occurs with permission errors or full disk.
    """
    pass


class FileNotFoundError(FileOperationError):
    """
    Exception raised when a file is not found.
    Occurs when specified file path doesn't exist.
    
    Note: Also aliased to builtin FileNotFoundError for compatibility.
    """
    pass


# ============ Validation Errors ============

class ValidationError(Exception):
    """
    Exception raised when input validation fails.
    Occurs with invalid parameters or data types.
    """
    pass


class InvalidParameterError(ValidationError):
    """
    Exception raised when function parameters are invalid.
    Occurs with None, wrong type, or out-of-range values.
    """
    pass


class DataTypeError(ValidationError):
    """
    Exception raised when data types don't match expectations.
    Occurs with incompatible type conversions or operations.
    """
    pass


# ============ Helper Functions ============

def get_exception_type(exception: Exception) -> str:
    """Get the exception type name."""
    return type(exception).__name__


def format_exception_message(exception_type: str, details: str, suggestion: str = None) -> str:
    """
    Format an exception message with type, details, and suggestion.
    
    Args:
        exception_type (str): Name of the exception
        details (str): Detailed error description
        suggestion (str, optional): Suggested fix or workaround
    
    Returns:
        str: Formatted error message
    """
    message = f"{exception_type}: {details}"
    if suggestion:
        message += f"\n  Suggestion: {suggestion}"
    return message
