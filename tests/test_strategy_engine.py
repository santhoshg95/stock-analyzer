"""
Strategy Engine Test
"""

import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.strategy.strategy_engine import StrategyEngine
from src.trading_engine.engine import TradingEngine


def main():

    engine = TradingEngine()

    report = engine.analyze("RELIANCE")

    strategy = StrategyEngine().evaluate(report)

    print("=" * 90)
    print("STRATEGY ENGINE")
    print("=" * 90)

    print(f"Strategy    : {strategy['strategy']}")
    print(f"Confidence  : {strategy['confidence']}%")
    print(f"Reason      : {strategy['reason']}")

    print("=" * 90)


if __name__ == "__main__":
    main()