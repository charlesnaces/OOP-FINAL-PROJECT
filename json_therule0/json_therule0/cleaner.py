# json_therule0/cleaner.py

import copy
try:
    # This works when the file is imported as part of a package
    from .loader import JSONLoader
except ImportError:
    # This is a fallback for when the script is run directly
    from loader import JSONLoader
import json

class JSONCleaner:
    """
    Uses a JSONLoader to load data and adds data cleaning capabilities.
    This class uses composition by containing a JSONLoader instance.
    """

    def __init__(self, filepath: str):
        """
        Initializes the JSONCleaner, which uses JSONLoader to load data.

        Args:
            filepath (str): The path to the .json file.
        """
        self.__loader = JSONLoader(filepath)
        self.filepath = filepath  # Store for __repr__
        self.__cleaned_data = copy.deepcopy(self.__loader.get_raw_data())

    def __repr__(self) -> str:
        """Overrides the parent __repr__ to include cleaning status."""
        raw_count = len(self.__loader.get_raw_data())
        cleaned_count = len(self.__cleaned_data)
        return (f"<{self.__class__.__name__} file='{self.filepath}' "
                f"raw_rows={raw_count} cleaned_rows={cleaned_count}>")

    def get_cleaned_data(self) -> list:
        """
        Provides access to the cleaned data.

        Returns:
            list: A list of dictionaries representing the cleaned JSON data.
        """
        return self.__cleaned_data

    def trim_whitespace(self):
        """
        Recursively trims leading/trailing whitespace from all string values.
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

    def remove_null_values(self):
        """
        Recursively removes key-value pairs where the value is None.
        """
        def recursive_remove_nulls(obj):
            if isinstance(obj, dict):
                # Iterate over a copy of keys since we might modify the dict
                for k in list(obj.keys()):
                    v = obj[k]
                    if v is None:
                        del obj[k]
                    else:
                        recursive_remove_nulls(v)
            elif isinstance(obj, list):
                # Iterate backwards when removing items to avoid index shifting issues
                for i in range(len(obj) - 1, -1, -1):
                    item = obj[i]
                    if item is None:
                        del obj[i]
                    else:
                        recursive_remove_nulls(item)

        recursive_remove_nulls(self.__cleaned_data)
        return self

    def flatten_json(self, separator: str = '_'):
        """
        Flattens all nested JSON objects in the list.

        Args:
            separator (str): The separator to use for joining nested keys.
        """
        flattened_list = []
        for record in self.__cleaned_data:
            flattened_dict = {}  # This will store the flattened record
            def flatten(obj, parent_key='', sep=separator):
                if isinstance(obj, dict):
                    for k, v in obj.items():
                        new_key = parent_key + sep + k if parent_key else k
                        flatten(v, new_key)
                elif isinstance(obj, list):
                    for i, item in enumerate(obj):
                        flatten(item, f"{parent_key}{sep}{i}" if parent_key else str(i))
                else:
                    flattened_dict[parent_key] = obj
            flatten(record)
            flattened_list.append(flattened_dict)
        self.__cleaned_data = flattened_list
        return self

    def remove_duplicates(self):
        """
        Removes duplicate records (dictionaries) from the data.
        """
        # Dictionaries are not hashable. We create a canonical string representation
        # using json.dumps with sorted keys to identify duplicates.
        seen = set()
        unique_data = []
        for record in self.__cleaned_data:
            # Create a hashable representation by converting the dict to a sorted JSON string.
            record_hash = json.dumps(record, sort_keys=True)
            if record_hash not in seen:
                seen.add(record_hash)
                unique_data.append(record)
        self.__cleaned_data = unique_data
        return self

    def convert_type(self, column: str, new_type: type, ignore_errors: bool = True):
        """
        Converts a specific column to a new data type.

        Args:
            column (str): The name of the column to convert.
            new_type (type): The target type to convert to (e.g., int, float, str).
            ignore_errors (bool): If True, values that can't be converted will be
                                  left as is. If False, a ValueError will be raised.
        """
        def recursive_convert(obj):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if k == column:
                        try:
                            # Don't try to convert if it's already the correct type
                            if not isinstance(v, new_type):
                                obj[k] = new_type(v)
                        except (ValueError, TypeError) as e:
                            if not ignore_errors:
                                raise ValueError(f"Could not convert value '{v}' "
                                                 f"in column '{k}' to {new_type.__name__}.") from e
                    else:
                        # Recurse into nested objects
                        recursive_convert(v)
            elif isinstance(obj, list):
                for item in obj:
                    recursive_convert(item)

        recursive_convert(self.__cleaned_data)
        return self

    def rename_key(self, old_key: str, new_key: str):
        """
        Recursively renames a key throughout the dataset.

        Args:
            old_key (str): The current name of the key.
            new_key (str): The new name for the key.
        """
        def recursive_rename(obj):
            if isinstance(obj, dict):
                # Use list() to create a copy of keys for safe iteration
                for k in list(obj.keys()):
                    v = obj[k]
                    if k == old_key:
                        # Pop the old key and assign its value to the new key
                        obj[new_key] = obj.pop(old_key)
                        # Continue recursion on the value, which is now under the new key
                        recursive_rename(obj[new_key])
                    else:
                        # Recurse into other values
                        recursive_rename(v)
            elif isinstance(obj, list):
                for item in obj:
                    recursive_rename(item)

        recursive_rename(self.__cleaned_data)
        return self


if __name__ == '__main__':
    """
    This block allows the script to be run directly for demonstration/testing.
    It will not run when the file is imported by other modules.
    """
    import os

    # Create a dummy JSON file for demonstration
    dummy_filepath = 'sample_data.json'
    dummy_data = [
        {"id": 1, "name": "  Test User 1  ", "details": {"age": 30, "city": "New York"}, "tags": ["a", "b"]},
        {"id": 2, "name": "Test User 2", "details": {"age": None, "city": "Los Angeles"}, "tags": ["c"]},
        {"id": 1, "name": "Test User 1", "details": {"age": 30, "city": "New York"}, "tags": ["a", "b"]}, # Duplicate
        {"id": 3, "name": "Test User 3", "details": None, "tags": ["a", "d"]}
    ]
    with open(dummy_filepath, 'w') as f:
        json.dump(dummy_data, f, indent=2)

    print(f"Created '{dummy_filepath}' for demonstration.")

    # --- Demonstrate JSONCleaner ---
    cleaner = JSONCleaner(dummy_filepath)
    print("\nInitial state:", cleaner)
    print("Initial data:", json.dumps(cleaner.get_cleaned_data(), indent=2))

    # Chain cleaning methods
    cleaner.trim_whitespace().remove_null_values().remove_duplicates().rename_key("name", "full_name")

    print("\nFinal state:", cleaner)
    print("Cleaned data:", json.dumps(cleaner.get_cleaned_data(), indent=2))

    # Clean up the dummy file
    os.remove(dummy_filepath)
    print(f"\nRemoved '{dummy_filepath}'.")
