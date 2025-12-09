# json_therule0/__init__.py

from .loader import JSONLoader
from .cleaner import JSONCleaner
from .analyzer import Analyzer
from .normalizer import Normalizer
from .jsonfile import JSONFile
from .api import read_json
from .exceptions import InvalidJSONError

# Backward compatibility
from .reader import JSONReader
from .advanced import AdvancedJSONReader

__all__ = [
    # Simple API (recommended)
    "read_json",
    "JSONFile",
    # Core modules
    "JSONLoader",
    "JSONCleaner",
    "Analyzer",
    "Normalizer",
    "InvalidJSONError",
    # Backward compatibility
    "JSONReader",
    "AdvancedJSONReader",
]

# Package version
__version__ = "0.1.1"

# Export version as well
__all__.append("__version__")
