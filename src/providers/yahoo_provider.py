"""
Yahoo Finance Provider
"""

import pandas as pd
import yfinance as yf

from src.providers.base_provider import BaseProvider


class YahooProvider(BaseProvider):

    @staticmethod
    def _flatten(df):

        if isinstance(df.columns, pd.MultiIndex):

            df.columns = df.columns.get_level_values(0)

        return df

    def get_historical_data(

        self,

        symbol,

        period="1y",

        interval="1d"

    ):

        ticker = symbol if symbol.startswith("^") else symbol + ".NS"

        df = yf.download(

            ticker,

            period=period,

            interval=interval,

            auto_adjust=True,

            progress=False

        )

        return self._flatten(df)

    def get_ltp(self, symbol):

        df = self.get_historical_data(

            symbol,

            period="5d"

        )

        if df.empty:

            return None

        return float(df["Close"].iloc[-1])

    def get_option_chain(self, symbol):

        raise NotImplementedError(

            "Yahoo provider does not support NSE option chain."

        )