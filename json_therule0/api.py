# json_therule0/api.py

from .jsonfile import JSONFile


def read_json(filepath: str) -> JSONFile:
    """
    Simple function to load and process a JSON file.
    Auto-handles loading, normalizing, and cleaning.

    Args:
        filepath (str): Path to JSON file.

    Returns:
        JSONFile: Processed data ready for analysis.

    Example:
        >>> data = read_json('data.json')
        >>> print(data.info())
        >>> print(data.summary())
        >>> data.to_csv('output.csv')
    """
    return JSONFile(filepath)
