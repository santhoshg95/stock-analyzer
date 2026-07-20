"""
Kite Market Data Provider
"""

from datetime import date, timedelta
from pathlib import Path

import pandas as pd
from kiteconnect import KiteConnect

from src.config.secrets import Secrets

from src.providers.base_provider import BaseProvider


class KiteProvider(BaseProvider):

    def __init__(self):

        self.kite = KiteConnect(
            api_key=Secrets.KITE_API_KEY
        )

        self.kite.set_access_token(
            Secrets.KITE_ACCESS_TOKEN
        )

    # -----------------------------------------------------

    def get_profile(self):

        return self.kite.profile()

    # -----------------------------------------------------

    def get_ltp(self, symbol):

        exchange_symbol = f"NSE:{symbol}"

        data = self.kite.ltp([exchange_symbol])

        return data[exchange_symbol]["last_price"]

    # -----------------------------------------------------

    def get_historical_data(

        self,

        symbol,

        period="1y",

        interval="day"

    ):

        instrument_token = self._instrument_token(symbol)
        from_date = self._from_date(period)
        kite_interval = {
            "1d": "day",
            "day": "day",
            "1h": "60minute",
            "60minute": "60minute",
            "30m": "30minute",
            "30minute": "30minute",
            "15m": "15minute",
            "15minute": "15minute",
            "5m": "5minute",
            "5minute": "5minute",
        }.get(interval)
        if kite_interval is None:
            raise ValueError(f"Unsupported Kite interval: {interval}")

        # Kite limits the date span per historical request. Daily ten-year
        # history is fetched in bounded chunks and then de-duplicated.
        candles = []
        chunk_start = from_date
        today = date.today()
        max_days = 1999 if kite_interval == "day" else 100
        while chunk_start <= today:
            chunk_end = min(chunk_start + timedelta(days=max_days), today)
            candles.extend(self.kite.historical_data(
                instrument_token, chunk_start, chunk_end, kite_interval,
            ))
            chunk_start = chunk_end + timedelta(days=1)
        dataframe = pd.DataFrame(candles)
        if dataframe.empty:
            return dataframe
        dataframe = dataframe.rename(
            columns={
                "date": "Date",
                "open": "Open",
                "high": "High",
                "low": "Low",
                "close": "Close",
                "volume": "Volume",
            }
        )
        dataframe["Date"] = pd.to_datetime(dataframe["Date"])
        dataframe = dataframe.drop_duplicates(subset=["Date"]).sort_values("Date")
        return dataframe.set_index("Date")[["Open", "High", "Low", "Close", "Volume"]]

    @staticmethod
    def _from_date(period: str) -> date:
        """Convert a small, explicit period vocabulary to a calendar date."""
        offsets = {
            "1mo": pd.DateOffset(months=1),
            "3mo": pd.DateOffset(months=3),
            "6mo": pd.DateOffset(months=6),
            "1y": pd.DateOffset(years=1),
            "2y": pd.DateOffset(years=2),
            "5y": pd.DateOffset(years=5),
            "10y": pd.DateOffset(years=10),
        }
        if period not in offsets:
            raise ValueError(f"Unsupported Kite period: {period}")
        return (pd.Timestamp.today().normalize() - offsets[period]).date()

    @staticmethod
    def _instrument_token(symbol: str) -> int:
        """Resolve an NSE equity token from the instrument-master reference file."""
        clean_symbol = symbol.upper().removesuffix(".NS")
        instrument_file = Path(__file__).resolve().parents[2] / "data" / "instruments.csv"
        if not instrument_file.exists():
            raise FileNotFoundError(
                "data/instruments.csv is required to resolve Kite instrument tokens"
            )
        instruments = pd.read_csv(instrument_file, usecols=["instrument_token", "tradingsymbol", "exchange", "instrument_type"])
        matches = instruments[
            (instruments["exchange"] == "NSE")
            & (instruments["instrument_type"] == "EQ")
            & (instruments["tradingsymbol"] == clean_symbol)
        ]
        if matches.empty:
            raise ValueError(f"No NSE equity instrument token found for {clean_symbol}")
        return int(matches.iloc[0]["instrument_token"])

    # -----------------------------------------------------

    def get_option_chain(

        self,

        symbol

    ):

        raise NotImplementedError(
            "Option Chain implementation coming next."
        )
