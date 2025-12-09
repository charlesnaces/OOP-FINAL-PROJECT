# json_therule0/loader.py

import json
from pathlib import Path
from typing import Union
from .exceptions import InvalidJSONError, MalformedJSONError, InvalidRootError

class JSONLoader:
    """
    Responsible for loading and validating a JSON file from a given path.
    """

    def __init__(self, filepath: Union[str, Path]):
        """
        Initializes the JSONLoader with the path to a JSON file.

        Args:
            filepath (str): The path to the .json file.
        """
        self.filepath = filepath
        self.__raw_data: list = []
        self.load()

    def __repr__(self) -> str:
        """Provides a developer-friendly representation of the JSONLoader object."""
        status = "loaded" if self.__raw_data is not None else "not loaded"
        return f"<{self.__class__.__name__} file='{self.filepath}' status='{status}'>"

    def __eq__(self, other) -> bool:
        """Compares two JSONLoader objects by filepath and data."""
        if not isinstance(other, JSONLoader):
            return False
        return self.filepath == other.filepath and self.__raw_data == other.__raw_data

    def __str__(self) -> str:
        """Returns a user-friendly string representation."""
        row_count = len(self.__raw_data) if self.__raw_data else 0
        return f"JSONLoader({self.filepath}) - {row_count} records"

    def load(self):
        """
        Reads and validates the JSON file.

        The parsed JSON data is stored in a private attribute `__raw_data`.
        It expects the top-level JSON structure to be a list of objects.

        Raises:
            FileNotFoundError: If the file does not exist at the specified path.
            MalformedJSONError: If the file is not a valid JSON.
            InvalidRootError: If the JSON root is not a list of objects.
        """
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError as e:
            # Re-raise the built-in FileNotFoundError to be explicit.
            raise FileNotFoundError(f"Error: File not found at '{self.filepath}'.") from e
        except json.JSONDecodeError as e:
            # Wrap the JSON decode error in our custom exception.
            raise MalformedJSONError(f"Error: Failed to decode JSON from '{self.filepath}'. Check file for syntax errors.") from e

        if not isinstance(data, list):
            raise InvalidRootError(f"JSON root in '{self.filepath}' must be a list of objects.")
        self.__raw_data = data

    def get_raw_data(self) -> list:
        """
        Provides access to the raw, unmodified data loaded from the file.

        Returns:
            list: A list of dictionaries representing the raw JSON data.
        """
        return self.__raw_data

    def load_and_process(self):
        """
        Default processing method: loads and validates the JSON file.
        This is the recommended way to load files.

        Returns:
            JSONLoader: Self for chaining, with data loaded and validated.
        """
        self.load()
        return self
