# json_therule0/analyzer.py

import csv
from collections import Counter
import json
import copy
from typing import List, Dict, Optional, Callable


class Analyzer:
    """
    Analyzes cleaned JSON data (a list of dictionaries).
    Provides read-only access with statistics, filtering, and export capabilities.
    This class combines analysis and advanced features in one unified interface.
    """

    def __init__(self, data: list):
        """
        Initializes the Analyzer with cleaned data.

        Args:
            data (list): A list of dictionaries (cleaned JSON records).
        
        Raises:
            TypeError: If the input data is not a list.
        """
        if not isinstance(data, list):
            raise TypeError("Input data for Analyzer must be a list of dictionaries.")
        
        self.__data = data
        self.__columns = self._discover_columns()
        self._analysis_cache = {}

    def _discover_columns(self) -> list:
        """Discovers all unique column names across all records."""
        column_set = set()
        for record in self.__data:
            if isinstance(record, dict):
                column_set.update(record.keys())
        return sorted(list(column_set))

    def _get_raw_data(self) -> List[Dict]:
        """Helper method to access private data."""
        return copy.deepcopy(self.__data)

    def __repr__(self) -> str:
        """Provides a summary representation of the analyzer object."""
        rows, cols = self.shape()
        return f"<{self.__class__.__name__} rows={rows} columns={cols}>"

    def __eq__(self, other) -> bool:
        """Compares two Analyzer objects by data and columns."""
        if not isinstance(other, Analyzer):
            return False
        return self.__data == other.__data and self.__columns == other.__columns

    def __str__(self) -> str:
        """Returns a user-friendly string representation."""
        rows, cols = self.shape()
        return f"Analyzer with {rows} rows and {cols} columns"

    def __len__(self) -> int:
        """Returns the number of records (rows) in the data."""
        return len(self.__data)

    # ============ Basic Analysis Methods ============

    def shape(self) -> tuple:
        """
        Returns the shape of the data as (number of rows, number of columns).

        Returns:
            tuple: A tuple containing the row count and column count.
        """
        return (len(self.__data), len(self.__columns))

    def get_columns(self) -> list:
        """
        Returns a sorted list of all unique column names in the data.

        Returns:
            list: A list of column name strings.
        """
        return self.__columns
    
    def columns(self) -> list:
        """Alias for get_columns() for compatibility."""
        return self.get_columns()

    def stats(self) -> dict:
        """
        Get statistics for each column.
        - Numeric: count, mean, std, min, 25%, 50%, 75%, max
        - Other: count, unique, top, freq

        Returns:
            dict: Statistics by column name.
        """
        stats = {}
        for col in self.__columns:
            values = [rec.get(col) for rec in self.__data if rec.get(col) is not None]
            
            if not values:
                stats[col] = {'count': 0}
                continue

            # Check if the column is numeric
            is_numeric = all(isinstance(v, (int, float)) for v in values)

            if is_numeric:
                values.sort()
                count = len(values)
                mean = sum(values) / count
                # Standard deviation
                variance = sum([(v - mean) ** 2 for v in values]) / count
                std = variance ** 0.5
                # Percentiles
                p25 = values[int(count * 0.25)]
                p50 = values[int(count * 0.50)]
                p75 = values[int(count * 0.75)]

                stats[col] = {
                    'count': count,
                    'mean': round(mean, 2),
                    'std': round(std, 2),
                    'min': values[0],
                    '25%': p25,
                    '50%': p50,
                    '75%': p75,
                    'max': values[-1]
                }
            else:
                # Categorical/string data
                count = len(values)
                value_counts = Counter(map(str, values))
                unique_count = len(value_counts)
                if value_counts:
                    top, freq = value_counts.most_common(1)[0]
                else:
                    top, freq = (None, 0)

                stats[col] = {
                    'count': count,
                    'unique': unique_count,
                    'top': top,
                    'freq': freq
                }
        return stats

    def filter_by_value(self, column: str, value) -> list:
        """
        Filter records by column value.

        Args:
            column (str): Column name.
            value: Value to match.

        Returns:
            list: Matching records.
        """
        return [copy.deepcopy(r) for r in self.__data if r.get(column) == value]

    def head(self, n: int = 5) -> list:
        """Get first n records (compatibility method)."""
        return self._get_raw_data()[:n]

    def tail(self, n: int = 5) -> list:
        """Get last n records (compatibility method)."""
        return self._get_raw_data()[-n:]

    def get_all(self) -> list:
        """Get all records (compatibility method)."""
        return self._get_raw_data()

    def to_csv(self, filepath: str, columns: Optional[List[str]] = None) -> None:
        """
        Export to CSV file.

        Args:
            filepath (str): Output file path.
            columns (list, optional): Columns to export. Defaults to all.
        """
        data = self._get_raw_data()
        cols_to_export = columns if columns else self.__columns

        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=cols_to_export)
            writer.writeheader()
            for record in data:
                writer.writerow({col: record.get(col, '') for col in cols_to_export})

    def to_json(self, filepath: str) -> None:
        """
        Export to JSON file.

        Args:
            filepath (str): Output file path.
        """
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self._get_raw_data(), f, indent=2)

    def analyze_default(self) -> Dict:
        """
        Run comprehensive analysis in one call.

        Returns:
            dict: Shape, columns, and stats.
        """
        return {
            'shape': self.shape(),
            'columns': self.get_columns(),
            'stats': self.stats()
        }
