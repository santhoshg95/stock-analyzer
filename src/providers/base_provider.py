"""
Base Market Data Provider
"""

from abc import ABC, abstractmethod


class BaseProvider(ABC):

    @abstractmethod
    def get_historical_data(
        self,
        symbol,
        period="1y",
        interval="1d"
    ):
        pass

    @abstractmethod
    def get_ltp(
        self,
        symbol
    ):
        pass

    @abstractmethod
    def get_option_chain(
        self,
        symbol
    ):
        pass