"""
Zerodha Option Chain Provider
"""

from src.options.providers.option_chain_provider import OptionChainProvider
from src.options.models.option_chain import OptionChain


class ZerodhaOptionProvider(OptionChainProvider):

    def __init__(self, kite_client):

        self.kite = kite_client

    def get_option_chain(self, symbol: str) -> OptionChain:

        raise NotImplementedError(
            "Option Chain download will be implemented next."
        )