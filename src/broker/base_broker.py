"""
Base Broker Interface
"""

from abc import ABC, abstractmethod


class BaseBroker(ABC):

    @abstractmethod
    def connect(self):
        """Connect to broker"""
        pass

    @abstractmethod
    def get_ltp(self, symbol):
        """Return latest traded price"""
        pass

    @abstractmethod
    def place_order(
        self,
        symbol,
        transaction_type,
        quantity,
        order_type="MARKET",
        price=None,
    ):
        """Place an order"""
        pass

    @abstractmethod
    def positions(self):
        """Current positions"""
        pass

    @abstractmethod
    def holdings(self):
        """Current holdings"""
        pass