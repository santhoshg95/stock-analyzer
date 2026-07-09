"""
Quote Service Test
"""

import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.services.quote_service import QuoteService


def main():

    service = QuoteService()

    symbols = [

        "SBIN",

        "RELIANCE",

        "ICICIBANK",

        "TCS"

    ]

    quotes = service.get_quotes(symbols)

    print("=" * 100)
    print("LIVE QUOTES")
    print("=" * 100)

    for symbol, quote in quotes.items():

        print(f"{symbol:15} ₹ {quote['ltp']}")

    print("=" * 100)


if __name__ == "__main__":
    main()