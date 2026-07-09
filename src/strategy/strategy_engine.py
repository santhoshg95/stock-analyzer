"""
Strategy Engine
"""

from src.strategy.pullback_strategy import PullbackStrategy


class StrategyEngine:

    def __init__(self):

        self.strategies = [

            PullbackStrategy()

        ]

    def evaluate(self, report):

        for strategy in self.strategies:

            result = strategy.evaluate(report)

            if result is not None:

                return result

        return {

            "strategy": "NO TRADE",

            "confidence": 80,

            "reason":

                "No strategy conditions matched."

        }