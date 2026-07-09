"""
Relative Strength Index (RSI)
"""

import pandas as pd


class RSIIndicator:

    @staticmethod
    def calculate(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:

        data = df.copy()

        # Handle MultiIndex columns returned by yfinance
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        if "Close" not in data.columns:
            raise ValueError("Close column not found.")

        delta = data["Close"].diff()

        gain = delta.where(delta > 0, 0.0)
        loss = -delta.where(delta < 0, 0.0)

        avg_gain = gain.rolling(window=period).mean()
        avg_loss = loss.rolling(window=period).mean()

        rs = avg_gain / avg_loss

        data["RSI"] = 100 - (100 / (1 + rs))

        return data