"""
Relative Strength Analyzer

Compares stock performance against NIFTY.
"""

import yfinance as yf
import pandas as pd


class RelativeStrength:

    @staticmethod
    def _prepare(df: pd.DataFrame) -> pd.DataFrame:
        """
        Flattens MultiIndex columns if present.
        """

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        return df

    @classmethod
    def analyze(cls, symbol):

        stock = yf.download(
            symbol + ".NS",
            period="6mo",
            interval="1d",
            auto_adjust=True,
            progress=False,
        )

        nifty = yf.download(
            "^NSEI",
            period="6mo",
            interval="1d",
            auto_adjust=True,
            progress=False,
        )

        if stock.empty or nifty.empty:
            return None

        stock = cls._prepare(stock)
        nifty = cls._prepare(nifty)

        stock_start = float(stock["Close"].iloc[0])
        stock_end = float(stock["Close"].iloc[-1])

        nifty_start = float(nifty["Close"].iloc[0])
        nifty_end = float(nifty["Close"].iloc[-1])

        stock_return = ((stock_end - stock_start) / stock_start) * 100

        market_return = ((nifty_end - nifty_start) / nifty_start) * 100

        rs = stock_return - market_return

        if rs >= 10:
            rating = "VERY STRONG"
        elif rs >= 5:
            rating = "STRONG"
        elif rs >= 0:
            rating = "OUTPERFORM"
        elif rs >= -5:
            rating = "INLINE"
        else:
            rating = "UNDERPERFORM"

        return {
            "stock_return": round(stock_return, 2),
            "market_return": round(market_return, 2),
            "relative_strength": round(rs, 2),
            "rating": rating,
        }