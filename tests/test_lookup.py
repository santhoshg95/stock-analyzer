"""
Instrument Lookup Test
"""

import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.instrument.instrument_service import InstrumentService


def main():

    service = InstrumentService()

    print("=" * 90)
    print("EQUITY LOOKUP")
    print("=" * 90)

    reliance = service.find_equity("RELIANCE")

    print(reliance)

    print()

    print("=" * 90)
    print("NIFTY OPTIONS")
    print("=" * 90)

    nifty = service.get_index_options("NIFTY")

    print(nifty.head())

    print()

    print(f"Total Contracts : {len(nifty)}")

    print("=" * 90)


if __name__ == "__main__":
    main()