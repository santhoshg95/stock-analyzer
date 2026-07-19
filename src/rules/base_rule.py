"""
Base Rule
"""

from abc import ABC, abstractmethod


class BaseRule(ABC):

    @abstractmethod
    def evaluate(self, context):
        pass