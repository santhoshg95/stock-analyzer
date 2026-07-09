"""
Global Market Provider
"""

from src.market_data.base_provider import BaseMarketProvider


class GlobalMarketProvider(BaseMarketProvider):

    SYMBOLS = {
        "dow_futures": "YM=F",
        "nasdaq_futures": "NQ=F",
        "sp500_futures": "ES=F",
        "nikkei": "^N225",
        "hang_seng": "^HSI",
    }

    def get_snapshot(self):

        return {
            name: self.download_symbol(symbol)
            for name, symbol in self.SYMBOLS.items()
        }