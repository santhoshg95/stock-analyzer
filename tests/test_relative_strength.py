"""
Relative Strength Test
"""

import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.market.relative_strength import RelativeStrength


def main():

    report = RelativeStrength.analyze("RELIANCE")

    print("=" * 90)
    print("RELATIVE STRENGTH")
    print("=" * 90)

    for key, value in report.items():

        print(f"{key:20}: {value}")

    print("=" * 90)


if __name__ == "__main__":
    main()