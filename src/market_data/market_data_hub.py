"""
Market Data Hub

Central place for retrieving all market-related data.

All engines (Market, Sector, News, Candidate, AI)
should consume data from this class instead of
calling providers directly.
"""

from datetime import datetime

from src.market_data.global_provider import GlobalMarketProvider
from src.market_data.india_provider import IndiaMarketProvider
from src.market_data.commodity_provider import CommodityProvider
from src.market_data.forex_provider import ForexProvider
from src.market_data.volatility_provider import VolatilityProvider


class MarketDataHub:

    def __init__(self):

        self.global_provider = GlobalMarketProvider()

        self.india_provider = IndiaMarketProvider()

        self.commodity_provider = CommodityProvider()

        self.forex_provider = ForexProvider()

        self.volatility_provider = VolatilityProvider()

    # -------------------------------------------------

    def get_market_snapshot(self):

        return {

            "timestamp": datetime.now(),

            "india": self.india_provider.get_snapshot(),

            "global": self.global_provider.get_snapshot(),

            "commodities": self.commodity_provider.get_snapshot(),

            "forex": self.forex_provider.get_snapshot(),

            "volatility": self.volatility_provider.get_snapshot()

        }