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
                        .get_cleaned_data())
        
        print(f"State after cleaning: {cleaner}")

        # 3. Pass the cleaned data to the reader for analysis
        print("\n--- Analysis of Cleaned Data ---")
        reader = JSONReader(cleaned_data)

        print(f"Reader object: {reader}")
        print(f"Shape of the data (rows, columns): {reader.shape()}")
        print(f"Columns: {reader.get_columns()}")
        print("\nSummary Statistics:")
        print(reader.summary_stats())

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()