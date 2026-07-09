"""
Adaptive AI Score Engine
"""

from src.factors.factor_engine import FactorEngine
from src.scoring.adaptive_weight_engine import AdaptiveWeightEngine
from src.scoring.ai_score_result import AIScoreResult


class AIScoreEngineV2:

    def __init__(self):

        self.factor_engine = FactorEngine()

    def calculate(self, context):

        report = self.factor_engine.evaluate(context)

        factors = report["factors"]

        weights = AdaptiveWeightEngine.get_weights(context)

        total = 0

        max_score = 0

        for factor in factors:

            weight = weights.get(factor.name, factor.weight)

            contribution = factor.score * weight

            factor.weight = weight
            factor.contribution = contribution

            total += contribution
            max_score += 100 * weight

        percentage = round((total / max_score) * 100, 2)

        if percentage >= 85:

            recommendation = "STRONG BUY"

        elif percentage >= 70:

            recommendation = "BUY"

        elif percentage >= 55:

            recommendation = "WATCH"

        else:

            recommendation = "WAIT"

        confidence = round(

            sum(f.confidence for f in factors) / len(factors),

            2

        )

        return AIScoreResult(

            total_score=round(total, 2),

            max_score=round(max_score, 2),

            percentage=percentage,

            factors=factors,

            recommendation=recommendation,

            confidence=confidence

        )