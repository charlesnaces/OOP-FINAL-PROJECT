# json_therule0/jsonfile.py

from .loader import JSONLoader
from .normalizer import Normalizer
from .cleaner import JSONCleaner
from .analyzer import Analyzer
from typing import List, Dict, Optional
import json


class JSONFile:
    """
    Simple, easy-to-use wrapper for processing JSON files.
    Handles loading, normalizing, cleaning, and analyzing in one unified interface.
    """

    def __init__(self, filepath: str):
        """
        Initialize and process JSON file with defaults.

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
        Auto-process: load, normalize, clean, and prepare for analysis.
        """
        # Try to load as-is, if it fails, try normalizing first
        try:
            # Load
            loader = JSONLoader(self.filepath)
            self._raw_data = loader.get_raw_data()
            self._normalized_data = self._raw_data
        except Exception:
            # If loading fails, try normalizing first
            normalizer = Normalizer(self.filepath)
            self._normalized_data = normalizer.normalize_auto()
            self._raw_data = None
        
        # Clean
        cleaner = JSONCleaner.__new__(JSONCleaner)
        cleaner._JSONCleaner__loader = None
        cleaner.filepath = self.filepath
        cleaner._JSONCleaner__cleaned_data = self._normalized_data.copy() if isinstance(self._normalized_data, list) else self._normalized_data
        self._cleaned_data = cleaner.clean_standard().get_cleaned_data()
        
        # Setup analyzer
        self._analyzer = Analyzer(self._cleaned_data)

    # ============ Simple Display Methods ============

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
        """
        Get statistical summary of the data.

        Returns:
            dict: Summary statistics.
        """
        return self._analyzer.summary_stats()

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
        """
        Get column names.

        Returns:
            list: Column names.
        """
        return self._analyzer.get_columns()

    def data(self) -> List[Dict]:
        """
        Get all data.

        Returns:
            list: All records.
        """
        return self._analyzer.get_all()

    # ============ Filtering & Selection ============

    def filter(self, column: str, value) -> 'JSONFile':
        """
        Filter by column value.

        Args:
            column (str): Column name.
            value: Value to match.

        Returns:
            JSONFile: New instance with filtered data.
        """
        filtered = self._analyzer.filter_by_value(column, value)
        new_file = JSONFile.__new__(JSONFile)
        new_file.filepath = self.filepath
        new_file._analyzer = filtered
        new_file._cleaned_data = filtered.get_all()
        new_file._normalized_data = None
        new_file._raw_data = None
        return new_file

    def select(self, columns: List[str]) -> 'JSONFile':
        """
        Select specific columns.

        Args:
            columns (list): Column names to keep.

        Returns:
            JSONFile: New instance with selected columns.
        """
        selected_data = [
            {col: record.get(col) for col in columns}
            for record in self._cleaned_data
        ]
        new_file = JSONFile.__new__(JSONFile)
        new_file.filepath = self.filepath
        new_file._analyzer = Analyzer(selected_data)
        new_file._cleaned_data = selected_data
        new_file._normalized_data = None
        new_file._raw_data = None
        return new_file

    # ============ Export ============

    def to_csv(self, filepath: str) -> None:
        """
        Export to CSV file.

        Args:
            filepath (str): Output file path.
        """
        self._analyzer.export_to_csv(filepath)
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
