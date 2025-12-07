# main.py

from json_therule0 import JSONCleaner, JSONReader

def main():
    """
    Demonstrates the end-to-end workflow of the json_therule0 library.
    """
    filepath = 'data.json'

    try:
        # 1. Initialize the cleaner, which automatically loads the data
        print(f"Loading and cleaning data from '{filepath}'...")
        cleaner = JSONCleaner(filepath)
        print(f"Initial state: {cleaner}")

        # 2. Chain cleaning operations
        cleaned_data = (cleaner
                        .trim_whitespace()
                        .remove_null_values()
                        .convert_type('price', float)
                        .remove_duplicates()
                        .get_cleaned_d