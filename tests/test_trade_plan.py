"""
Trade Plan Test
"""

import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.data_provider.provider import DataProvider
from src.indicators.pipeline import IndicatorPipeline
from src.trade_setup.entry_analyzer import EntryAnalyzer
from src.trade_plan.trade_plan import TradePlanEngine


def main():

    provider = DataProvider()

    df = provider.get_data("RELIANCE")

    if df is None:

        print("Unable to load data.")

        return

    df = IndicatorPipeline.run(df)

    entry = EntryAnalyzer.analyze(df)

    trade = TradePlanEngine.generate(entry)

    print("=" * 90)
    print("TRADE PLAN")
    print("=" * 90)

    print(f"Entry           : ₹{trade.entry}")

    print(f"Stop Loss       : ₹{trade.stop_loss}")

    print(f"Target 1        : ₹{trade.target1}")

    print(f"Target 2        : ₹{trade.target2}")

    print(f"Risk            : ₹{trade.risk}")

    print(f"Reward          : ₹{trade.reward}")

    print(f"Risk Reward     : {trade.risk_reward}")

    print(f"Quality         : {trade.quality}")

    print("=" * 90)


if __name__ == "__main__":

    main()