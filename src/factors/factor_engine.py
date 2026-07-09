"""
Factor Engine

Combines all available factors.
"""

from src.factors.market_factor import MarketFactor
from src.factors.technical_factor import TechnicalFactor


class FactorEngine:

    def __init__(self):

        self.factors = [

            MarketFactor(),

            TechnicalFactor()

        ]

    def evaluate(self, context):

        results = []

        total = 0

        for factor in self.factors:

            result = factor.evaluate(context)

            results.append(result)

            total += result.contribution

        return {

            "factors": results,

            "score": round(total, 2)

        }