"""
Technical Factor
"""

from src.factors.base_factor import BaseFactor
from src.factors.factor_result import FactorResult


class TechnicalFactor(BaseFactor):

    WEIGHT = 0.30

    def evaluate(self, context):

        technical = context.technical

        score = technical.confidence

        contribution = score * self.WEIGHT

        return FactorResult(

            name="TECHNICAL",

            score=score,

            weight=self.WEIGHT,

            confidence=technical.confidence,

            contribution=contribution,

            reasons=technical.reasons,

            metadata=technical.metadata

        )