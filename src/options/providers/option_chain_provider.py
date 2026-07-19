"""
Option Chain Provider

Base interface for all option chain providers.
"""

from abc import ABC, abstractmethod

from src.options.models.option_chain import OptionChain


class OptionChainProvider(ABC):

    @abstractmethod
    def get_option_chain(self, symbol: str) -> OptionChain:
        """
        Return complete option chain.
        """
        raise NotImplementedError