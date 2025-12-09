# json_therule0/__init__.py

from .loader import JSONLoader
from .cleaner import JSONCleaner
from .analyzer import Analyzer
from .normalizer import Normalizer
from .exceptions import InvalidJSONError

# Backward compatibility
from .reader import JSONReader
from .advanced import AdvancedJSONReader

__all__ = [
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
