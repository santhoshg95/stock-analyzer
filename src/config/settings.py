"""
Global Project Configuration
"""

from pathlib import Path

# Root folder for downloaded market data
DATA_FOLDER = Path("data/raw")

# Default download settings
DEFAULT_PERIOD = "2y"
DEFAULT_INTERVAL = "1d"

# NSE Stocks suffix
NSE_SUFFIX = ".NS"