"""
Category Score Test
"""

import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.trading_engine.engine import TradingEngine
from src.scoring.category_score import CategoryScoreEngine


def main():

    engine = TradingEngine()

    report = engine.analyze("RELIANCE")

    result = CategoryScoreEngine.calculate(report)

    print("=" * 90)
    print("CATEGORY SCORE")
    print("=" * 90)

    for name, score in result["categories"].items():

        print(f"{name:20}: {score}")

    print()

    print("=" * 90)

    print(f"Overall Score : {result['overall']}/100")

    print("=" * 90)


if __name__ == "__main__":
    main()