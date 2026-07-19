"""
Option Provider Factory
"""

from src.broker.kite_auth import KiteAuthentication
from src.options.providers.zerodha_option_provider import (
    ZerodhaOptionProvider,
)


class OptionProviderFactory:

    @staticmethod
    def create():

        auth = KiteAuthentication()

        kite = auth.get_client()

        return ZerodhaOptionProvider(kite)