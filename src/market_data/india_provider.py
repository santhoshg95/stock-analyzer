"""
India Market Provider

Downloads Indian market indices.
"""

from src.market_data.base_provider import BaseMarketProvider


class IndiaMarketProvider(BaseMarketProvider):

    def __init__(self):

        self.symbols = {

            "nifty": "^NSEI",

            "banknifty": "^NSEBANK",

            "finnifty": "NIFTY_FIN_SERVICE.NS"

        }

    def get_snapshot(self):

        data = {}

        for name, symbol in self.symbols.items():

            snapshot = self.download_symbol(symbol)

            if snapshot is not None:

                data[name] = snapshot

        return data