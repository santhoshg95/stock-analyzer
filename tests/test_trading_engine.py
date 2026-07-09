"""
Trading Engine Test
"""

import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.trading_engine.engine import TradingEngine


def main():

    engine = TradingEngine()

    report = engine.analyze("RELIANCE")

    if report is None:

        print("Unable to analyze stock.")

        return

    analysis = report["analysis"]

    print("=" * 90)
    print("AI TRADING ENGINE REPORT")
    print("=" * 90)

    print(f"Stock               : {analysis.symbol}")
    print(f"Current Price       : ₹{analysis.current_price:.2f}")
    print(f"Trend               : {analysis.trend}")
    print(f"Overall Score       : {analysis.score}/100")
    print(f"Recommendation      : {analysis.recommendation}")

    print()

    print("=" * 90)
    print("ENTRY ANALYSIS")
    print("=" * 90)

    for key, value in report["entry"].items():

        print(f"{key:22}: {value}")

    print()

    print("=" * 90)
    print("BREAKOUT ANALYSIS")
    print("=" * 90)

    breakout = report["breakout"]

    print(f"Confirmed           : {breakout['confirmed']}")
    print(f"Conditions Passed   : {breakout['score']}/{breakout['total_conditions']}")

    print()

    for name, status in breakout["conditions"].items():

        print(f"{name:25}: {status}")

    print()

    print("=" * 90)
    print("FINAL AI DECISION")
    print("=" * 90)

    decision = report["decision"]

    print(f"Action              : {decision['action']}")
    print(f"Confidence          : {decision['confidence']}%")
    print(f"Reason              : {decision['reason']}")

    print("=" * 90)


if __name__ == "__main__":

    main()