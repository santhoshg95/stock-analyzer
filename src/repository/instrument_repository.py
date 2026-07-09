"""
Instrument Repository

Loads Zerodha Instrument Master once and provides
fast lookup methods.
"""

from pathlib import Path

import pandas as pd


class InstrumentRepository:

    FILE = Path("data/instruments.csv")

    def __init__(self):

        if not self.FILE.exists():
            raise FileNotFoundError(
                "Instrument file not found. "
                "Run test_instruments.py first."
            )

        self.df = pd.read_csv(self.FILE)

        self._build_indexes()

    # -------------------------------------------------------

    def _build_indexes(self):

        self.symbol_index = {}

        self.token_index = {}

        for _, row in self.df.iterrows():

            symbol = str(row["tradingsymbol"]).upper()

            self.symbol_index[symbol] = row

            self.token_index[int(row["instrument_token"])] = row

    # -------------------------------------------------------

    def get_by_symbol(self, symbol):

        return self.symbol_index.get(symbol.upper())

    # -------------------------------------------------------

    def get_by_token(self, token):

        return self.token_index.get(token)

    # -------------------------------------------------------

    def filter(
        self,
        exchange=None,
        segment=None,
        name=None,
        instrument_type=None,
    ):

        df = self.df

        if exchange:
            df = df[df["exchange"] == exchange]

        if segment:
            df = df[df["segment"] == segment]

        if name:
            df = df[df["name"] == name]

        if instrument_type:
            df = df[df["instrument_type"] == instrument_type]

        return df.reset_index(drop=True)