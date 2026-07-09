"""
Live Option Chain Builder
"""

import pandas as pd

from src.instrument.instrument_service import InstrumentService
from src.market.quote_service import QuoteService
from src.providers.provider_factory import ProviderFactory


class LiveOptionChain:

    def __init__(self):

        self.provider = ProviderFactory.create("kite")

        self.instrument_service = InstrumentService()

        self.quote_service = QuoteService(
            self.provider.kite
        )

    # --------------------------------------------------------

    def build(self, underlying):

        contracts = self.instrument_service.get_index_options(
            underlying
        )

        option_contracts = contracts[
            contracts["instrument_type"].isin(["CE", "PE"])
        ]

        symbols = [

            f"NFO:{symbol}"

            for symbol in option_contracts["tradingsymbol"]

        ]

        print()

        print(f"Contracts : {len(symbols)}")

        print()

        quotes = self.quote_service.get_quotes(
            symbols,
            batch_size=200
        )

        rows = []

        for _, row in option_contracts.iterrows():

            exchange_symbol = f"NFO:{row['tradingsymbol']}"

            if exchange_symbol not in quotes:
                continue

            q = quotes[exchange_symbol]

            buy_depth = q.get("depth", {}).get("buy", [])
            sell_depth = q.get("depth", {}).get("sell", [])

            bid = buy_depth[0]["price"] if buy_depth else None
            ask = sell_depth[0]["price"] if sell_depth else None

            rows.append({

                "tradingsymbol": row["tradingsymbol"],

                "expiry": row["expiry"],

                "strike": row["strike"],

                "type": row["instrument_type"],

                "ltp": q.get("last_price"),

                "oi": q.get("oi"),

                "volume": q.get("volume"),

                "bid": bid,

                "ask": ask

            })

        return pd.DataFrame(rows)