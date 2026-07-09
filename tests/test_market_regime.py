"""
Market Regime Test
"""

import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.market.market_regime import MarketRegime
from src.market_data.market_data_hub import MarketDataHub


def main():

    hub = MarketDataHub()

    snapshot = hub.get_market_snapshot()

    report = MarketRegime.classify(snapshot)

    print("=" * 100)
    print("MARKET REGIME")
    print("=" * 100)

    print(f"Engine       : {report.engine}")
    print(f"Regime       : {report.status}")
    print(f"Score        : {report.score}")
    print(f"Confidence   : {report.confidence}%")

    print()

    print("Reasons")
    print("-" * 100)

    for reason in report.reasons:

        print(f"✓ {reason}")

    if report.warnings:

        print()

        print("Warnings")
        print("-" * 100)

        for warning in report.warnings:

            print(f"⚠ {warning}")

    print("=" * 100)


if __name__ == "__main__":

    main()