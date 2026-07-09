"""
Volatility Provider
"""

from src.market_data.base_provider import BaseMarketProvider


class VolatilityProvider(BaseMarketProvider):

    def get_snapshot(self):

        return self.download_symbol("^INDIAVIX")