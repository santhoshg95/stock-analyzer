"""
Breakout Detector Test
"""

import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.data_provider.provider import DataProvider
from src.indicators.pipeline import IndicatorPipeline
from src.breakout.breakout_detector import BreakoutDetector


def main():

    provider = DataProvider()

    df = provider.get_data("RELIANCE")

    df = IndicatorPipeline.run(df)

    result = BreakoutDetector.analyze(df)

    print("=" * 80)
    print("BREAKOUT TEST")
    print("=" * 80)

    for k, v in result.items():

        print(f"{k:20}: {v}")


if __name__ == "__main__":

    main()