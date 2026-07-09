"""
Moving Average Convergence Divergence (MACD)
"""

import pandas as pd


class MACDIndicator:

    @staticmethod
    def calculate(df: pd.DataFrame) -> pd.DataFrame:

        data = df.copy()

        # Flatten MultiIndex columns returned by yfinance
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        if "Close" not in data.columns:
            raise ValueError("Close column not found.")

        # Fast EMA
        ema12 = data["Close"].ewm(span=12, adjust=False).mean()

        # Slow EMA
        ema26 = data["Close"].ewm(span=26, adjust=False).mean()

        # MACD Line
        data["MACD"] = ema12 - ema26

        # Signal Line
        data["MACD_SIGNAL"] = (
            data["MACD"]
            .ewm(span=9, adjust=False)
            .mean()
        )

        # Histogram
        data["MACD_HISTOGRAM"] = (
            data["MACD"]
            - data["MACD_SIGNAL"]
        )

        return data