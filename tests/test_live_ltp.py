"""
Live LTP Test
"""

import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.providers.provider_factory import ProviderFactory


def main():

    provider = ProviderFactory.create("kite")

    print("=" * 90)
    print("LIVE MARKET DATA")
    print("=" * 90)

    stocks = [

        "RELIANCE",

        "SBIN",

        "ICICIBANK",

        "TCS"

    ]

    for stock in stocks:

        price = provider.get_ltp(stock)

        print(f"{stock:15} ₹ {price}")

    print("=" * 90)


if __name__ == "__main__":

    main()