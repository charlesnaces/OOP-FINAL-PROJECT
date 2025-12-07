# main.py

from pathlib import Path
import pprint
from json_therule0 import JSONCleaner, JSONReader
import argparse

def main(filepath: Path):
    """
    Demonstrates the end-to-end workflow of the json_therule0 library.

    Args:
        filepath (Path): The path to the JSON file to process.
    """
    try:
        if not filepath.exists():
            print(f"Error: File not found at '{filepath}'. Please ensure it's in the 'data' directory.")
            return

        # 1. Initialize the cleaner, which automatically loads the data
        print(f"Loading and cleaning data from '{filepath}'...")
        cleaner = JSONCleaner(filepath)
        print(f"Initial state: {cleaner}")

        # 2. Chain cleaning operations
        # Note: We rename 'user' to 'user_data' to demonstrate the feature.
        cleaned_data = (cleaner
                        .trim_whitespace()
                        .remove_null_values()
                        .rename_key('user', 'user_data')
                        .remove_duplicates()
                        .get_cleaned_data())
        
        print(f"State after cleaning: {cleaner}")

        # 3. Pass the cleaned data to the reader for analysis
        print("\n--- Analysis of Cleaned Data ---")
        reader = JSONReader(cleaned_data)

        print(f"Reader object: {reader}")
        print(f"Shape of the data (rows, columns): {reader.shape()}")
        print(f"Columns: {reader.get_columns()}")
        
        print("\nSummary Statistics:")
        # Use pprint for a more readable dictionary output
        pprint.pprint(reader.summary_stats())

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Set up the command-line argument parser
    parser = argparse.ArgumentParser(
        description="Cleans and analyzes a JSON file."
    )
    
    # Define the 'filepath' argument
    parser.add_argument(
        "filepath",
        type=Path,
        nargs='?',  # Makes the argument optional
        default=Path(__file__).parent / 'data' / 'sample_data.json',  # Default value
        help="Path to the JSON file in the 'data' directory. Defaults to 'data/sample_data.json'."
    )

    args = parser.parse_args()
    main(args.filepath)