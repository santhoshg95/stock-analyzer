"""
Average True Range (ATR)
"""

import pandas as pd


class ATRIndicator:

    @staticmethod
    def calculate(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:

        data = df.copy()

        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        if not {"High", "Low", "Close"}.issubset(data.columns):
            raise ValueError("High, Low, Close columns are required.")

        previous_close = data["Close"].shift(1)

        tr1 = data["High"] - data["Low"]

        tr2 = (data["High"] - previous_close).abs()

        tr3 = (data["Low"] - previous_close).abs()

        true_range = pd.concat(
            [tr1, tr2, tr3],
            axis=1
        ).max(axis=1)

        data["ATR"] = true_range.rolling(period).mean()

        return data