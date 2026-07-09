"""
Indicator Pipeline

This module executes all technical indicators in sequence.
Every indicator receives a DataFrame and returns an updated DataFrame.

Pipeline Order:
1. EMA
2. RSI
3. MACD
4. ATR
5. Volume
"""

import pandas as pd

from src.indicators.ema import EMAIndicator
from src.indicators.rsi import RSIIndicator
from src.indicators.macd import MACDIndicator
from src.indicators.atr import ATRIndicator
from src.indicators.volume import VolumeIndicator


class IndicatorPipeline:
    """
    Runs all indicators on the historical data.
    """

    @staticmethod
    def run(df: pd.DataFrame) -> pd.DataFrame:

        # Trend
        df = EMAIndicator.calculate(df)

        # Momentum
        df = RSIIndicator.calculate(df)

        # Momentum Confirmation
        df = MACDIndicator.calculate(df)

        # Volatility
        df = ATRIndicator.calculate(df)

        # Volume Analysis
        df = VolumeIndicator.calculate(df)

        return df