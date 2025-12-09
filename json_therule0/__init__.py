# json_therule0/__init__.py

from .loader import JSONLoader
from .cleaner import JSONCleaner
from .reader import JSONReader
from .advanced import AdvancedJSONReader
from .exceptions import InvalidJSONError

__all__ = [
    "JSONLoader",
    "JSONCleaner",
    "JSONReader",
    "AdvancedJSONReader",
    "InvalidJSONError"
]

# Package version
__version__ = "0.1.1"

# Export version as well
__all__.append("__version__")
