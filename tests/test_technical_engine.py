"""
Technical Engine Test
"""

import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.technical.technical_engine import TechnicalEngine


def main():

    engine = TechnicalEngine()

    report = engine.analyze("SBIN")

    print("=" * 100)
    print("TECHNICAL ENGINE")
    print("=" * 100)

    print(f"Engine       : {report.engine}")
    print(f"Status       : {report.status}")
    print(f"Score        : {report.score}")
    print(f"Confidence   : {report.confidence}")

    print()

    print("Reasons")
    print("-" * 100)

    for reason in report.reasons:
        print(f"✓ {reason}")

    print()

    print("Metadata")
    print("-" * 100)

    for key, value in report.metadata.items():
        print(f"{key:15}: {value}")

    print("=" * 100)


if __name__ == "__main__":
    main()