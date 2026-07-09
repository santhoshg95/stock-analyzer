"""
Multi Timeframe Test
"""

import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.multi_timeframe.trend_alignment import MultiTimeframeAnalyzer


def main():

    result = MultiTimeframeAnalyzer.analyze("RELIANCE")

    print("=" * 90)
    print("MULTI TIMEFRAME ANALYSIS")
    print("=" * 90)

    for tf, trend in result.items():

        print(f"{tf:15}: {trend}")

    print("=" * 90)


if __name__ == "__main__":

    main()