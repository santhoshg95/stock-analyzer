"""
Provider Factory
"""

from src.providers.yahoo_provider import YahooProvider
from src.providers.kite_provider import KiteProvider


class ProviderFactory:

    @staticmethod
    def create(name):

        providers = {

            "yahoo": YahooProvider(),

            "kite": KiteProvider()

        }

        if name.lower() not in providers:

            raise ValueError(
                f"Unknown provider : {name}"
            )

        return providers[name.lower()]