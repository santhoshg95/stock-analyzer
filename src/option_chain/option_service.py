"""
Option Chain Service

Business layer for option chain.
"""

from src.providers.provider_factory import ProviderFactory


class OptionChainService:

    def __init__(

        self,

        provider_name="yahoo"

    ):

        self.provider = ProviderFactory.create(provider_name)

    def get_option_chain(

        self,

        symbol

    ):

        return self.provider.get_option_chain(symbol)