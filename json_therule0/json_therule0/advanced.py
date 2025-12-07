# json_therule0/advanced.py

import csv
from typing import List, Dict, Optional
from .reader import JSONReader


class AdvancedJSONReader(JSONReader):
    """
    Extends JSONReader with advanced data analysis capabilities.
    
    This subclass demonstrates inheritance and polymorphism by adding
    specialized methods for data export, filtering, and transformation.
    """

    def __init__(self, data: List[Dict]):
        """
        Initializes the AdvancedJSONReader with cleaned data.

        Args:
            data (list): A list of dictionaries (cleaned JSON records).
        """
        super().__init__(data)
        self._analysis_cache = {}

    def _get_raw_data(self) -> List[Dict]:
        """Helper method to access parent's private data."""
        # Using getattr to access parent's private __data attribute safely
        return getattr(self, '_JSONReader__data', [])

    def export_to_csv(self, filepath: str, columns: Optional[List[str]] = None) -> None:
        """
        Exports the data to a CSV file.

        Args:
            filepath (str): The path where the CSV will be saved.
            columns (list, optional): Specific columns to export. Defaults to all columns.
        """
        data = self._get_raw_data()
        cols_to_export = columns if columns else self.get_columns()

        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=cols_to_export)
            writer.writeheader()
            for record in data:
                writer.writerow({col: record.get(col, '') for col in cols_to_export})

    def filter_by_value(self, column: str, value) -> 'AdvancedJSONReader':
        """
        Filters data by a specific column value and returns a new AdvancedJSONReader.

        Args:
            column (str): The column name to filter on.
            value: The value to match.

        Returns:
            AdvancedJSONReader: A new instance with filtered data.
        """
        data = self._get_raw_data()
        filtered = [record for record in data if record.get(column) == value]
        return AdvancedJSONReader(filtered)

    def get_unique_values(self, column: str) -> List:
        """
        Returns unique values for a given column.

        Args:
            column (str): The column name.

        Returns:
            list: A sorted list of unique values.
        """
        data = self._get_raw_data()
        unique = set()
        for record in data:
            if column in record:
                value = record[column]
                # Handle unhashable types like dicts
                try:
                    unique.add(value)
                except TypeError:
                    pass
        return sorted([v for v in unique if v is not None], key=str)

    def describe(self) -> Dict:
        """
        Returns a detailed description of the dataset.

        Returns:
            dict: Contains row count, column count, columns list, and summary statistics.
        """
        rows, cols = self.shape()

        return {
            'rows': rows,
            'columns': cols,
            'column_names': self.get_columns(),
            'summary_stats': self.summary_stats()
        }

    def __repr__(self) -> str:
        """Override repr to show this is an advanced reader."""
        rows, cols = self.shape()
        return f"<AdvancedJSONReader rows={rows} columns={cols}>"
