# json_therule0/__init__.py

from .processor import Processor
from .analyzer import Analyzer
from .normalizer import Normalizer
from .jsonfile import JSONFile
from .api import read_json
from .exceptions import InvalidJSONError

__all__ = [
    # Simple API (recommended)
    "read_json",
    "JSONFile",
    # Core modules
    "Processor",
    "Analyzer",
    "Normalizer",
    "InvalidJSONError",
]

# Package version
__version__ = "0.1.1"

# Export version as well
__all__.append("__version__")
