from pathlib import Path
from single_version import get_version

__version__ = get_version('backend', Path(__file__).parent.parent)
