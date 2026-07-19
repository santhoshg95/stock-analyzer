"""
Factor Engine

Combines all intelligence modules into one AI score.
"""

from src.context.stock_context import StockContext

from src.factors.models.factor_analysis import FactorAnalysis
from src.factors.models.factor_score import FactorScore


class FactorEngine:

    def analyze(
        self,
        context: StockContext,
    ) -> FactorAnalysis:

        analysis = FactorAnalysis()

        # ----------------------------------------------------
        # Option Factor
        # ----------------------------------------------------

        if (
            context.options
            and context.options.analysis
        ):

            option = context.options.analysis

            factor = FactorScore(

                name="Options",

                score=option.score,

                confidence=option.confidence,

                weight=0.30,

                reason=", ".join(option.reasons),

            )

            analysis.factors.append(factor)

        # ----------------------------------------------------
        # Future modules
        # ----------------------------------------------------

        # Technical

        # News

        # Market

        # Sector

        # Fundamentals

        # Sentiment

        if not analysis.factors:
            return analysis

        total_weight = sum(f.weight for f in analysis.factors)

        weighted_score = sum(
            f.score * f.weight
            for f in analysis.factors
        )

        weighted_confidence = sum(
            f.confidence * f.weight
            for f in analysis.factors
        )

        analysis.overall_score = round(
            weighted_score / total_weight,
            2,
        )

        analysis.confidence = round(
            weighted_confidence / total_weight,
            2,
        )

        for factor in analysis.factors:

            if factor.score >= 70:
                analysis.bullish_factors += 1

            elif factor.score <= 40:
                analysis.bearish_factors += 1

            else:
                analysis.neutral_factors += 1

        return analysis