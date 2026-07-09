"""
Backtesting Test
"""

import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.backtesting.backtester import Backtester
from src.backtesting.metrics import Metrics
from src.data_provider.provider import DataProvider
from src.indicators.pipeline import IndicatorPipeline


def main():

    provider = DataProvider()

    df = provider.get_data("RELIANCE")

    df = IndicatorPipeline.run(df)

    trades = Backtester.run(df)

    report = Metrics.summarize(trades)

    print("=" * 90)
    print("BACKTEST REPORT")
    print("=" * 90)

    for key, value in report.items():

        print(f"{key:20}: {value}")

    print("=" * 90)


if __name__ == "__main__":

    main()