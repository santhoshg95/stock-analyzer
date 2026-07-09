"""
F&O Universe Test
"""

import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.universe.fo_universe import FOUniverse


def main():

    universe = FOUniverse()

    symbols = universe.get_symbols()

    print("=" * 100)
    print("F&O UNIVERSE")
    print("=" * 100)

    print(f"Total Stocks : {len(symbols)}")

    print()

    print("First 50 Symbols")

    print("-" * 100)

    for symbol in symbols[:50]:

        print(symbol)

    print("=" * 100)


if __name__ == "__main__":

    main()