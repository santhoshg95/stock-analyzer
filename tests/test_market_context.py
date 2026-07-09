"""
Market Context Test
"""

import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.market.market_context import MarketContext


def main():

    report = MarketContext.analyze()

    print("=" * 90)
    print("MARKET CONTEXT")
    print("=" * 90)

    for market, data in report.items():

        print(f"{market:15}")

        print(f"Trend : {data['trend']}")

        print(f"Close : {data['close']}")

        print("-" * 90)


if __name__ == "__main__":

    main()