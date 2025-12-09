# json_therule0/exceptions.py

class InvalidJSONError(Exception):
    """Custom exception for errors related to invalid JSON format."""
    pass

class MalformedJSONError(InvalidJSONError):
    """Exception raised when JSON decoding fails."""
    pass

class InvalidRootError(InvalidJSONError):
    """Exception raised when the JSON root is not a list of objects."""
    pass