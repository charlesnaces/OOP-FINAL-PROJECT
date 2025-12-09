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
        1. Try Processor (load + clean)
        2. If InvalidRootError: Try Normalizer first, then Processor
        3. Finally pass to Analyzer
        """
        try:
            # Try standard processing
            processor = Processor(self.filepath)
            self._raw_data = processor.get_raw_data()
            processor.clean()
            self._cleaned_data = processor.get_cleaned_data()
            self._normalized_data = self._cleaned_data
            
        except InvalidRootError as e:
            # Data is unstructured, use Normalizer
            print(f"ℹ️  Detected unstructured JSON. Using Normalizer...")
            normalizer = Normalizer(self.filepath)
            self._normalized_data = normalizer.normalize_auto()
            self._raw_data = None
            
            # Clean the normalized data
            processor = Processor.__new__(Processor)
            processor._Processor__raw_data = self._normalized_data
            processor._Processor__cleaned_data = copy.deepcopy(self._normalized_data)
            processor.filepath = self.filepath
            processor.clean()
            self._cleaned_data = processor.get_cleaned_data()
            
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
        return self._analyzer.get_all()[:n]

    def tail(self, n: int = 5) -> List[Dict]:
        """
        Show last n records.

        Args:
            n (int): Number of records to show.

        Returns:
            list: Last n records.
        """
        return self._analyzer.get_all()[-n:]

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
        return self._analyzer.get_all()

    # ============ Filtering ============

    def filter(self, column: str, value) -> list:
        """Filter by column value, return matching records."""
        return self._analyzer.filter_by_value(column, value)

    # ============ Export ============

    def to_csv(self, filepath: str) -> None:
        """Export to CSV file."""
        self._analyzer.to_csv(filepath)
        print(f"✓ Exported to {filepath}")

    def to_json(self, filepath: str) -> None:
        """
        Export to JSON file.

        Args:
            filepath (str): Output file path.
        """
        import json
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self._cleaned_data, f, indent=2)
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
