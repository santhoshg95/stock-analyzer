"""
Sector Strength Test
"""

import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.sector.sector_strength import SectorStrength


def main():

    engine = SectorStrength()

    report = engine.analyze()

    print("=" * 100)
    print("SECTOR STRENGTH")
    print("=" * 100)

    for sector, data in sorted(report.items()):

        print(

            f"{sector:18}"

            f"{data['change_percent']:>8.2f}%"

            f"   {data['rating']:10}"

            f" Score : {data['score']}"

        )

    print("=" * 100)


if __name__ == "__main__":
    main()