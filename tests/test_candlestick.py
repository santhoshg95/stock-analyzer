"""
Candlestick Pattern Test
"""

import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.candlestick.pattern_detector import PatternDetector
from src.data_provider.provider import DataProvider
from src.indicators.pipeline import IndicatorPipeline


def main():

    provider = DataProvider()

    df = provider.get_data("RELIANCE")

    df = IndicatorPipeline.run(df)

    result = PatternDetector.detect(df)

    print("=" * 80)
    print("CANDLESTICK PATTERN")
    print("=" * 80)

    print(f"Pattern   : {result['pattern']}")
    print(f"Signal    : {result['signal']}")
    print(f"Strength  : {result['strength']}")

    print("=" * 80)


if __name__ == "__main__":
    main()