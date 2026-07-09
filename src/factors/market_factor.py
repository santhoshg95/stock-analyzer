"""
Market Factor
"""

from src.factors.base_factor import BaseFactor
from src.factors.factor_result import FactorResult


class MarketFactor(BaseFactor):

    WEIGHT = 0.20

    def evaluate(self, context):

        market = context.market

        score = market.confidence

        contribution = score * self.WEIGHT

        return FactorResult(

            name="MARKET",

            score=score,

            weight=self.WEIGHT,

            confidence=market.confidence,

            contribution=contribution,

            reasons=market.reasons,

            metadata=market.metadata

        )