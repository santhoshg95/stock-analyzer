"""
Base Strategy
"""

from abc import ABC, abstractmethod


class BaseStrategy(ABC):

    @abstractmethod
    def evaluate(self, report):

        pass