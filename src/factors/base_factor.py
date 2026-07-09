"""
Base Factor
"""

from abc import ABC, abstractmethod

from src.context.stock_context import StockContext


class BaseFactor(ABC):

    @abstractmethod
    def evaluate(self, context: StockContext):
        pass