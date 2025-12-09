# examples/basic_usage.py
"""
Comprehensive examples for using the json_therule0 library.
Demonstrates the simple API and core functionality.
"""

from json_therule0 import read_json

# ==============================================================================
# EXAMPLE 1: Basic Loading and Display
# ==============================================================================

def example_basic_loading():
    """Load a JSON file and display basic information."""
    print("=" * 70)
    print("EXAMPLE 1: Basic Loading and Display")
    print("=" * 70)
    
    # Load the JSON file
    data = read_json('../data/sample_data.json')
    
    # Display basic information
    print(data.info())
    print()


# ==============================================================================
# EXAMPLE 2: Viewing Data
# ==============================================================================

def example_viewing_data():
    """View first and last records, plus summary statistics."""
    print("=" * 70)
    print("EXAMPLE 2: Viewing Data")
    print("=" * 70)
    
    data = read_json('../data/sample_data.json')
    
    # View first 3 records
    print("First 3 records:")
    for i, record in enumerate(data.head(3), 1):
        print(f"  {i}. {record}")
    print()
    
    # View last 2 records
    print("Last 2 records:")
    for i, record in enumerate(data.tail(2), 1):
        print(f"  {i}. {record}")
    print()
    
    # Get comprehensive summary with statistics
    print(data.summary())
    print()


# ==============================================================================
# EXAMPLE 3: Filtering Data
# ==============================================================================

def example_filtering():
    """Filter data by column values."""
    print("=" * 70)
    print("EXAMPLE 3: Filtering Data")
    print("=" * 70)
    
    data = read_json('../data/sample_data.json')
    
    # Example: Filter by a specific value
    # Replace 'category' and 'value' with actual column names from your data
    try:
        # Get column names first
        columns = data.columns()
        print(f"Available columns: {columns}\n")
        
        # Filter example (if 'status' column exists)
        if 'status' in columns:
            results = data.filter('status', 'active')
            print(f"Found {len(results)} records with status='active'")
            if results:
                print(f"Sample: {results[0]}\n")
    except ValueError as e:
        print(f"Filter error: {e}\n")


# ==============================================================================
# EXAMPLE 4: Selecting Columns
# ==============================================================================

def example_selecting_columns():
    """Select specific columns from data."""
    print("=" * 70)
    print("EXAMPLE 4: Selecting Columns")
    print("=" * 70)
    
    data = read_json('../data/sample_data.json')
    
    columns = data.columns()
    print(f"Available columns: {columns}\n")
    
    # Select specific columns (using actual column names)
    try:
        if len(columns) >= 2:
            selected_cols = columns[:2]  # Select first 2 columns
            print(f"Selecting columns: {selected_cols}")
            results = data.select(selected_cols)
            print(f"First record after selection: {results[0]}\n")
    except ValueError as e:
        print(f"Selection error: {e}\n")


# ==============================================================================
# EXAMPLE 5: Sorting Data
# ==============================================================================

def example_sorting():
    """Sort data by columns."""
    print("=" * 70)
    print("EXAMPLE 5: Sorting Data")
    print("=" * 70)
    
    data = read_json('../data/sample_data.json')
    
    columns = data.columns()
    print(f"Available columns: {columns}\n")
    
    # Sort by first column in ascending order
    try:
        if columns:
            col = columns[0]
            print(f"Sorting by column '{col}' (ascending):")
            sorted_data = data.sort(col, ascending=True)
            print(f"First 3 sorted records:")
            for record in sorted_data[:3]:
                print(f"  {record}")
            print()
            
            # Sort in descending order
            print(f"Sorting by column '{col}' (descending):")
            sorted_desc = data.sort(col, ascending=False)
            print(f"First 3 sorted records (descending):")
            for record in sorted_desc[:3]:
                print(f"  {record}")
            print()
    except ValueError as e:
        print(f"Sort error: {e}\n")


# ==============================================================================
# EXAMPLE 6: Statistics and Analysis
# ==============================================================================

def example_statistics():
    """Get statistical summaries of data."""
    print("=" * 70)
    print("EXAMPLE 6: Statistics and Analysis")
    print("=" * 70)
    
    data = read_json('../data/sample_data.json')
    
    # Get statistics for all columns
    stats = data.stats()
    
    print("Statistical Summary:")
    print("-" * 70)
    for column, column_stats in stats.items():
        print(f"\n{column}:")
        for stat_name, stat_value in column_stats.items():
            print(f"  {stat_name}: {stat_value}")
    print()


# ==============================================================================
# EXAMPLE 7: Exporting Data
# ==============================================================================

def example_exporting():
    """Export data to different formats."""
    print("=" * 70)
    print("EXAMPLE 7: Exporting Data")
    print("=" * 70)
    
    data = read_json('../data/sample_data.json')
    
    # Export to CSV
    print("Exporting to CSV format...")
    data.to_csv('../data/exported_data.csv')
    
    # Export to JSON
    print("Exporting to JSON format...")
    data.to_json('../data/exported_data.json')
    
    print()


# ==============================================================================
# EXAMPLE 8: Data Shape and Structure
# ==============================================================================

def example_data_structure():
    """Inspect data shape and structure."""
    print("=" * 70)
    print("EXAMPLE 8: Data Shape and Structure")
    print("=" * 70)
    
    data = read_json('../data/sample_data.json')
    
    # Get shape
    rows, cols = data.shape()
    print(f"Data shape: {rows} rows × {cols} columns")
    print(f"Total records: {len(data)}")
    print()
    
    # List all columns
    print("Columns:")
    for i, col in enumerate(data.columns(), 1):
        print(f"  {i}. {col}")
    print()


# ==============================================================================
# EXAMPLE 9: Handling Structured Data (COCO Format)
# ==============================================================================

def example_coco_format():
    """Handle structured data like COCO format."""
    print("=" * 70)
    print("EXAMPLE 9: Handling COCO Format Data")
    print("=" * 70)
    
    try:
        data = read_json('../data/coco_sample.json')
        print(f"Loaded COCO format data with {len(data)} records")
        print(data.info())
        print()
    except Exception as e:
        print(f"Note: COCO example skipped ({type(e).__name__})\n")


# ==============================================================================
# EXAMPLE 10: Combining Operations
# ==============================================================================

def example_combined_operations():
    """Demonstrate combining multiple operations."""
    print("=" * 70)
    print("EXAMPLE 10: Combining Operations")
    print("=" * 70)
    
    data = read_json('../data/sample_data.json')
    
    print("Workflow: Load → View Info → Export")
    print("-" * 70)
    
    # Get basic info
    rows, cols = data.shape()
    print(f"Loaded {rows} records with {cols} columns")
    
    # View sample data
    print(f"\nFirst record:")
    first = data.head(1)
    if first:
        print(f"  {first[0]}")
    
    # Export results
    print(f"\nExporting to CSV...")
    data.to_csv('../data/combined_export.csv')
    print("✓ Export complete!")
    print()


# ==============================================================================
# Main Execution
# ==============================================================================

def main():
    """Run all examples."""
    examples = [
        example_basic_loading,
        example_viewing_data,
        example_data_structure,
        example_filtering,
        example_selecting_columns,
        example_sorting,
        example_statistics,
        example_exporting,
        example_coco_format,
        example_combined_operations,
    ]
    
    for example_func in examples:
        try:
            example_func()
        except Exception as e:
            print(f"Error in {example_func.__name__}: {e}\n")


if __name__ == '__main__':
    main()
