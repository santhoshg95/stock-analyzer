"""
Position Size Test
"""

import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.position_sizing.position_size import PositionSizingEngine
from src.trade_plan.trade_plan import TradePlanEngine
from src.trade_setup.entry_analyzer import EntryAnalyzer
from src.data_provider.provider import DataProvider
from src.indicators.pipeline import IndicatorPipeline


def main():

    provider = DataProvider()

    df = provider.get_data("RELIANCE")

    df = IndicatorPipeline.run(df)

    entry = EntryAnalyzer.analyze(df)

    trade = TradePlanEngine.generate(entry)

    result = PositionSizingEngine.calculate(

        capital=1_000_000,

        risk_percent=1,

        entry=trade["entry"],

        stop_loss=trade["stop_loss"]

    )

    print("=" * 90)
    print("POSITION SIZE")
    print("=" * 90)

    print(f"Capital            : ₹10,00,000")

    print(f"Risk Per Trade     : 1%")

    print()

    for key, value in result.items():

        print(f"{key:20}: {value}")

    print("=" * 90)


if __name__ == "__main__":
    main()