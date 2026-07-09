"""
Test Entry Analyzer

Run:

python tests/test_entry.py
"""

import os
import sys

# ---------------------------------------------------------
# Add Project Root
# ---------------------------------------------------------

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# ---------------------------------------------------------

from src.data_provider.provider import DataProvider
from src.indicators.pipeline import IndicatorPipeline
from src.trade_setup.entry_analyzer import EntryAnalyzer


def main():

    symbol = "RELIANCE"

    print("=" * 80)
    print("ENTRY ANALYZER TEST")
    print("=" * 80)

    provider = DataProvider()

    df = provider.get_data(symbol)

    if df is None:

        print("No data found.")

        return

    print("Historical Data Loaded")

    df = IndicatorPipeline.run(df)

    print("Indicators Calculated")

    result = EntryAnalyzer.analyze(df)

    print()

    print("=" * 80)

    print("ENTRY REPORT")

    print("=" * 80)

    for key, value in result.items():

        print(f"{key:22}: {value}")

    print("=" * 80)


if __name__ == "__main__":

    main()