# json_therule0/reader.py

from collections import Counter
import json

class JSONReader:
    """
    Provides read-only analysis of cleaned JSON data (a list of dictionaries).
    This class is designed to work with the output of JSONCleaner.
    """

    def __init__(self, data: list):
        """
        Initializes the JSONReader with cleaned data.

        Args:
            data (list): A list of dictionaries (cleaned JSON records).
        
        Raises:
            TypeError: If the input data is not a list.
        """
        if not isinstance(data, list):
            raise TypeError("Input data for JSONReader must be a list of dictionaries.")
        
        self.__data = data
        self.__columns = self._discover_columns()

    def _discover_columns(self) -> list:
        """Discovers all unique column names across all records."""
        column_set = set()
        for record in self.__data:
            if isinstance(record, dict):
                column_set.update(record.keys())
        return sorted(list(column_set))

    def __repr__(self) -> str:
        """Provides a summary representation of the reader object."""
        rows, cols = self.shape()
        return f"<{self.__class__.__name__} rows={rows} columns={cols}>"

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

    def summary_stats(self) -> dict:
        """
        Generates descriptive statistics for each column.
        - For numeric columns: count, mean, std, min, 25%, 50%, 75%, max.
        - For non-numeric columns: count, unique, top, freq.

        Returns:
            dict: A dictionary where keys are column names and values are
                  dictionaries of statistics.
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
                value_counts = Counter(map(str, values)) # Use str to handle mixed types
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
