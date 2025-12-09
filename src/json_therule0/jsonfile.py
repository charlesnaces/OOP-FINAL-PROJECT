# json_therule0/jsonfile.py

import copy
import json
from typing import List, Dict, Optional
from .processor import Processor
from .normalizer import Normalizer
from .analyzer import Analyzer
from .exceptions import InvalidRootError, MalformedJSONError


class JSONFile:
    """
    Simple, pandas-like interface for processing JSON files.
    Auto-handles loading, normalizing, cleaning, and analyzing.
    
    Tries standard processing first. If data is unstructured, 
    automatically uses Normalizer to convert it.
    """

    def __init__(self, filepath: str):
        """
        Initialize and process JSON file with smart exception handling.

        Args:
            filepath (str): Path to the JSON file.
        """
        self.filepath = filepath
        self._raw_data = None
        self._normalized_data = None
        self._cleaned_data = None
        self._analyzer = None
        
        # Auto-process on init
        self._process()

    def _process(self):
        """
        Auto-process with intelligent exception handling.
        
        Flow:
        1. Try Processor (load + clean + auto-convert types)
        2. If InvalidRootError: Try Normalizer first, then Processor
        3. Finally pass to Analyzer
        """
        try:
            # Try standard processing
            processor = Processor(self.filepath)
            self._raw_data = processor.get_raw_data()
            processor.clean()
            processor.auto_convert_types()
            self._cleaned_data = processor.get_cleaned_data()
            self._normalized_data = self._cleaned_data
            
        except InvalidRootError as e:
            # Data is unstructured, use Normalizer
            normalizer = Normalizer(self.filepath)
            self._normalized_data = normalizer.normalize_auto()
            normalizer.auto_convert_types()  # Auto-convert types for normalized data
            self._cleaned_data = normalizer.normalized_data
            self._raw_data = None
            
        except Exception as e:
            # Other errors (file not found, malformed JSON, etc.)
            raise type(e)(str(e)) from e
        
        # Setup analyzer with cleaned data
        self._analyzer = Analyzer(self._cleaned_data)

    # ============ Display Methods ============

    def head(self, n: int = 5) -> List[Dict]:
        """
        Show first n records.

        Args:
            n (int): Number of records to show.

        Returns:
            list: First n records.
        """
        return self._analyzer._get_raw_data()[:n]

    def tail(self, n: int = 5) -> List[Dict]:
        """
        Show last n records.

        Args:
            n (int): Number of records to show.

        Returns:
            list: Last n records.
        """
        return self._analyzer._get_raw_data()[-n:]

    def info(self) -> str:
        """
        Show basic information about the data.

        Returns:
            str: Formatted information.
        """
        rows, cols = self._analyzer.shape()
        columns = self._analyzer.get_columns()
        
        output = []
        output.append("=" * 60)
        output.append(f"Dataset Info")
        output.append("=" * 60)
        output.append(f"Rows: {rows}")
        output.append(f"Columns: {cols}")
        output.append(f"\nColumn Names:")
        for i, col in enumerate(columns, 1):
            output.append(f"  {i}. {col}")
        output.append("=" * 60)
        
        return "\n".join(output)

    def stats(self) -> Dict:
        """Get statistical summary of the data."""
        return self._analyzer.stats()

    def summary(self) -> str:
        """
        Get complete summary (info + stats in readable format).

        Returns:
            str: Formatted summary.
        """
        rows, cols = self._analyzer.shape()
        
        output = []
        output.append("=" * 60)
        output.append(f"Summary")
        output.append("=" * 60)
        output.append(f"Rows: {rows}, Columns: {cols}")
        output.append("")
        output.append("Statistics:")
        
        stats = self.stats()
        for col, stat in stats.items():
            output.append(f"\n{col}:")
            for key, value in stat.items():
                output.append(f"  {key}: {value}")
        
        output.append("=" * 60)
        return "\n".join(output)

    # ============ Data Access ============

    def shape(self) -> tuple:
        """
        Get shape of data (rows, columns).

        Returns:
            tuple: (row_count, column_count)
        """
        return self._analyzer.shape()

    def columns(self) -> List[str]:
        """Get column names."""
        return self._analyzer.get_columns()

    def data(self) -> List[Dict]:
        """
        Get all data.

        Returns:
            list: All records.
        """
        return self._analyzer._get_raw_data()

    # ============ Filtering ============

    def filter(self, column: str, value) -> list:
        """
        Filter by column value, return matching records.
        
        Args:
            column (str): Column name to filter by.
            value: Value to match.
            
        Returns:
            list: Records where column equals value.
            
        Raises:
            ValueError: If column doesn't exist in the data.
        """
        available_columns = self._analyzer.get_columns()
        if column not in available_columns:
            raise ValueError(
                f"Column '{column}' not found. Available columns: {', '.join(available_columns)}"
            )
        return self._analyzer.filter_by_value(column, value)

    def select(self, columns: list) -> List[Dict]:
        """
        Select specific columns from the data.
        
        Args:
            columns (list): List of column names to include.
            
        Returns:
            list: Records with only selected columns.
            
        Raises:
            ValueError: If any column doesn't exist.
        """
        available_columns = set(self._analyzer.get_columns())
        requested_columns = set(columns)
        missing = requested_columns - available_columns
        
        if missing:
            raise ValueError(
                f"Columns not found: {', '.join(missing)}. Available: {', '.join(available_columns)}"
            )
        
        data = self._analyzer._get_raw_data()
        return [
            {col: record.get(col) for col in columns}
            for record in data
        ]

    def sort(self, column: str, ascending: bool = True) -> List[Dict]:
        """
        Sort data by a column.
        
        Args:
            column (str): Column to sort by.
            ascending (bool): Sort in ascending order. Defaults to True.
            
        Returns:
            list: Sorted records.
            
        Raises:
            ValueError: If column doesn't exist.
        """
        available_columns = self._analyzer.get_columns()
        if column not in available_columns:
            raise ValueError(
                f"Column '{column}' not found. Available columns: {', '.join(available_columns)}"
            )
        
        data = self._analyzer._get_raw_data()
        try:
            return sorted(data, key=lambda x: x.get(column, ''), reverse=not ascending)
        except TypeError:
            # Handle mixed types by converting to string for sorting
            return sorted(data, key=lambda x: str(x.get(column, '')), reverse=not ascending)

    # ============ Export ============

    def to_csv(self, filepath: str, verbose: bool = False) -> None:
        """
        Export to CSV file.
        
        Args:
            filepath (str): Output file path.
            verbose (bool): Print confirmation message. Defaults to False.
        """
        self._analyzer.to_csv(filepath)
        if verbose:
            print(f"✓ Exported to {filepath}")

    def to_json(self, filepath: str, verbose: bool = False) -> None:
        """
        Export to JSON file.

        Args:
            filepath (str): Output file path.
            verbose (bool): Print confirmation message. Defaults to False.
        """
        import json
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self._cleaned_data, f, indent=2)
        if verbose:
            print(f"✓ Exported to {filepath}")

    def __repr__(self) -> str:
        """String representation."""
        rows, cols = self.shape()
        return f"<JSONFile rows={rows} columns={cols}>"

    def __str__(self) -> str:
        """User-friendly representation."""
        rows, cols = self.shape()
        return f"JSONFile with {rows} rows and {cols} columns"

    def __len__(self) -> int:
        """Number of records."""
        return self.shape()[0]

    def display_record(self, index: int = 0, max_depth: int = None) -> None:
        """
        Display a single record with intelligent formatting for nested data.
        
        Handles deeply nested structures by indenting and showing hierarchy clearly.
        Works with lists, dicts, and mixed nested types.

        Args:
            index (int): Record index to display (0-based). Defaults to 0.
            max_depth (int): Maximum nesting depth to display. None = unlimited.
            
        Raises:
            IndexError: If index is out of range.
            
        Example:
            >>> data = read_json('api_response.json')
            >>> data.display_record(0)  # Show first record
            >>> data.display_record(2, max_depth=3)  # Show 3rd record, limit depth
        """
        import json
        
        if index < 0 or index >= len(self):
            raise IndexError(f"Record index {index} out of range (0-{len(self)-1})")
        
        record = self.data()[index]
        
        # Use json.dumps with indent for pretty printing
        # This automatically handles all nesting levels
        json_str = json.dumps(record, indent=2, default=str)
        
        # If max_depth specified, truncate output
        if max_depth is not None:
            lines = json_str.split('\n')
            max_indent = max_depth * 2
            truncated_lines = []
            
            for line in lines:
                # Count leading spaces
                indent = len(line) - len(line.lstrip())
                if indent > max_indent:
                    # Skip deeply nested lines
                    if '...truncated...' not in truncated_lines[-1] if truncated_lines else False:
                        truncated_lines.append(' ' * max_indent + '...truncated at depth ' + str(max_depth) + '...')
                else:
                    truncated_lines.append(line)
            
            json_str = '\n'.join(truncated_lines)
        
        print(json_str)
    
    def peek(self, index: int = 0) -> Dict:
        """
        Get a single record as dict for inspection.
        
        Shorthand for accessing and inspecting one record.
        
        Args:
            index (int): Record index to peek at (0-based).
            
        Returns:
            dict: The record at that index.
            
        Example:
            >>> record = data.peek(0)
            >>> print(record['name'])
        """
        if index < 0 or index >= len(self):
            raise IndexError(f"Record index {index} out of range (0-{len(self)-1})")
        return self.data()[index]
