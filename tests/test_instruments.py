"""
Instrument Master Test
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

    df = service.download()

    print("=" * 90)
    print("INSTRUMENT MASTER")
    print("=" * 90)

    print(df.head())

    print()

    print(f"Total Instruments : {len(df)}")

    print("=" * 90)


if __name__ == "__main__":

    main()