"""
India VIX Test
"""

import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.market.vix import IndiaVIX


def main():

    report = IndiaVIX.analyze()

    print("=" * 90)
    print("INDIA VIX")
    print("=" * 90)

    for k, v in report.items():

        print(f"{k:20}: {v}")

    print("=" * 90)


if __name__ == "__main__":
    main()