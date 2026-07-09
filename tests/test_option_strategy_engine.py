"""
Option Strategy Engine Test
"""

import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.option_strategy.option_strategy_engine import OptionStrategyEngine
from src.pipeline.analysis_pipeline import AnalysisPipeline


def main():

    pipeline = AnalysisPipeline()

    analysis = pipeline.analyze("SBIN")

    engine = OptionStrategyEngine()

    report = engine.recommend(analysis)

    print("=" * 100)
    print("OPTION STRATEGY ENGINE")
    print("=" * 100)

    print(f"Symbol : {report.symbol}")
    print(f"Reason : {report.reason}")

    print("\nRecommended Strategies")
    print("-" * 100)

    for strategy in report.recommended:

        print(f"✓ {strategy.name}")
        print(f"  Bias        : {strategy.market_bias}")
        print(f"  Volatility  : {strategy.volatility}")
        print(f"  Description : {strategy.description}")
        print()

    print("=" * 100)


if __name__ == "__main__":
    main()