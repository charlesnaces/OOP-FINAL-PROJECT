# json_therule0/processor.py

import json
import copy
from pathlib import Path
from typing import Union
from .exceptions import MalformedJSONError, InvalidRootError


class Processor:
    """
    Loads JSON files and cleans the data in one unified class.
    Combines loading and cleaning operations for a complete data processing workflow.
    """

    def __init__(self, filepath: Union[str, Path]):
        """
        Initialize Processor with a JSON file.
        Automatically loads and prepares data for cleaning.

        Args:
            filepath (str or Path): Path to the JSON file.
            
        Raises:
            FileNotFoundError: If file doesn't exist.
            MalformedJSONError: If JSON is invalid.
            InvalidRootError: If JSON root is not a list.
        """
        self.filepath = filepath
        self.__raw_data: list = []
        self.__cleaned_data: list = []
        self._load()

    def _load(self):
        """
        Load and validate JSON file.
        Expects top-level structure to be a list of objects.
        
        Raises:
            FileNotFoundError: If file doesn't exist.
            MalformedJSONError: If JSON is invalid.
            InvalidRootError: If JSON root is not a list.
        """
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Error: File not found at '{self.filepath}'.") from e
        except json.JSONDecodeError as e:
            raise MalformedJSONError(
                f"Error: Failed to decode JSON from '{self.filepath}'. Check file for syntax errors."
            ) from e

        if not isinstance(data, list):
            raise InvalidRootError(
                f"JSON root in '{self.filepath}' must be a list of objects. "
                f"Got {type(data).__name__} instead. Try using Normalizer for unstructured JSON."
            )
        
        self.__raw_data = data
        self.__cleaned_data = copy.deepcopy(self.__raw_data)

    def __repr__(self) -> str:
        """Developer-friendly representation."""
        raw_count = len(self.__raw_data)
        cleaned_count = len(self.__cleaned_data)
        return (f"<Processor file='{self.filepath}' "
                f"raw={raw_count} cleaned={cleaned_count}>")

    def __eq__(self, other) -> bool:
        """Compare two Processor objects."""
        if not isinstance(other, Processor):
            return False
        return self.filepath == other.filepath and self.__cleaned_data == other.__cleaned_data

    def __str__(self) -> str:
        """User-friendly representation."""
        return f"Processor({self.filepath}) - {len(self.__cleaned_data)} records"

    # ============ Data Access ============

    def get_raw_data(self) -> list:
        """
        Get the original unmodified data from the file.

        Returns:
            list: Raw data as loaded from JSON.
        """
        return copy.deepcopy(self.__raw_data)

    def get_cleaned_data(self) -> list:
        """
        Get the cleaned data.

        Returns:
            list: Cleaned data after all operations.
        """
        return copy.deepcopy(self.__cleaned_data)

    # ============ Cleaning Methods ============

    def trim(self):
        """
        Trim leading/trailing whitespace from all string values.
        
        Returns:
            Processor: Self for method chaining.
        """
        def recursive_trim(obj):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    obj[k] = recursive_trim(v)
            elif isinstance(obj, list):
                for i, elem in enumerate(obj):
                    obj[i] = recursive_trim(elem)
            return obj.strip() if isinstance(obj, str) else obj

        recursive_trim(self.__cleaned_data)
        return self

    def drop_null(self):
        """
        Remove key-value pairs where the value is None.
        
        Returns:
            Processor: Self for method chaining.
        """
        def recursive_remove_nulls(obj):
            if isinstance(obj, dict):
                for k in list(obj.keys()):
                    v = obj[k]
                    if v is None:
                        del obj[k]
                    else:
                        recursive_remove_nulls(v)
            elif isinstance(obj, list):
                for i in range(len(obj) - 1, -1, -1):
                    item = obj[i]
                    if item is None:
                        del obj[i]
                    else:
                        recursive_remove_nulls(item)

        recursive_remove_nulls(self.__cleaned_data)
        return self

    def drop_duplicates(self):
        """
        Remove duplicate records from the data.
        
        Returns:
            Processor: Self for method chaining.
        """
        seen = set()
        unique_data = []
        for record in self.__cleaned_data:
            record_hash = json.dumps(record, sort_keys=True)
            if record_hash not in seen:
                seen.add(record_hash)
                unique_data.append(record)
        self.__cleaned_data = unique_data
        return self

    def clean(self):
        """
        Apply standard cleaning: trim whitespace, drop nulls, drop duplicates.
        
        Returns:
            Processor: Self for method chaining.
        """
        return (self
                .trim()
                .drop_null()
                .drop_duplicates())

    def load_and_process(self):
        """
        Default processing method: load and clean in one call.
        This is the recommended way to process files.

        Returns:
            Processor: Self for chaining.
        """
        self.clean()
        return self
