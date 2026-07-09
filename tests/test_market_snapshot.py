"""
Market Snapshot Test
"""

import os
import sys
from pprint import pprint

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.market_data.market_data_hub import MarketDataHub


def main():

    hub = MarketDataHub()

    snapshot = hub.get_market_snapshot()

    print("=" * 100)
    print("MARKET SNAPSHOT")
    print("=" * 100)

    pprint(snapshot)

    print("=" * 100)


if __name__ == "__main__":
    main()