"""
Exponential Moving Average (EMA)
"""

import pandas as pd


class EMAIndicator:
    """
    Calculates Exponential Moving Averages
    """

    @staticmethod
    def calculate(df: pd.DataFrame) -> pd.DataFrame:

        data = df.copy()

        # yfinance may return MultiIndex columns
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        if "Close" not in data.columns:
            raise ValueError("Close column not found in dataframe.")

        data["EMA20"] = data["Close"].ewm(span=20, adjust=False).mean()

        data["EMA50"] = data["Close"].ewm(span=50, adjust=False).mean()

        data["EMA200"] = data["Close"].ewm(span=200, adjust=False).mean()

        return data