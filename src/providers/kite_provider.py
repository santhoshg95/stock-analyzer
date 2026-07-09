"""
Kite Market Data Provider
"""

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

        data = self.kite.ltp(
            exchange_symbol
        )

        return data[exchange_symbol]["last_price"]

    # -----------------------------------------------------

    def get_historical_data(

        self,

        symbol,

        period="1y",

        interval="day"

    ):

        raise NotImplementedError(
            "Historical data implementation will use instrument tokens."
        )

    # -----------------------------------------------------

    def get_option_chain(

        self,

        symbol

    ):

        raise NotImplementedError(
            "Option Chain implementation coming next."
        )