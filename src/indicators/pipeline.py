"""
Indicator Pipeline

Applies all technical indicators to a dataframe.
"""

import pandas as pd

from src.indicators.ema import EMAIndicator
from src.indicators.rsi import RSIIndicator


class IndicatorPipeline:

    @staticmethod
    def run(df: pd.DataFrame) -> pd.DataFrame:
        """
        Execute all indicators in sequence.
        """

        df = EMAIndicator.calculate(df)
        df = RSIIndicator.calculate(df)

        return df