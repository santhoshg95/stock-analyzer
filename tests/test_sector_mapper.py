"""
Sector Mapper Test
"""

import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.sector.sector_mapper import SectorMapper


def main():

    mapper = SectorMapper()

    print("=" * 100)
    print("SECTOR LOOKUP")
    print("=" * 100)

    symbols = [
        "SBIN",
        "ICICIBANK",
        "INFY",
        "TCS",
        "RELIANCE",
        "LT",
        "SUNPHARMA",
        "TATASTEEL"
    ]

    for symbol in symbols:

        sector = mapper.get_sector(symbol)

        print(f"{symbol:15} {sector}")

    print()

    print("=" * 100)
    print("ALL SECTORS")
    print("=" * 100)

    for sector in mapper.get_all_sectors():

        print(sector)

    print()

    print("=" * 100)
    print("BANKING STOCKS")
    print("=" * 100)

    stocks = mapper.get_sector_stocks("BANKING")

    for stock in stocks:

        print(stock)

    print("=" * 100)


if __name__ == "__main__":

    main()
