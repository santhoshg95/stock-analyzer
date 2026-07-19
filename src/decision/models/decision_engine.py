"""
Decision Engine

Converts FactorAnalysis into a trading decision.
"""

from src.context.stock_context import StockContext

from src.decision.models.decision import Decision


class DecisionEngine:
    """
    Generates BUY / SELL / HOLD decisions.
    """

    def decide(
        self,
        context: StockContext,
    ) -> Decision:

        if context.factors is None:

            return Decision(

                action="NO_DATA",

                confidence=0,

                score=0,

                reasons=["Factor analysis not available."],

            )

        factors = context.factors

        score = factors.overall_score

        confidence = factors.confidence

        # ----------------------------------------------------
        # Decision Logic
        # ----------------------------------------------------

        if score >= 85:

            action = "STRONG_BUY"

        elif score >= 70:

            action = "BUY"

        elif score >= 45:

            action = "HOLD"

        elif score >= 30:

            action = "SELL"

        else:

            action = "STRONG_SELL"

        reasons = []

        for factor in factors.factors:

            reasons.append(

                f"{factor.name}: {factor.reason}"

            )

        return Decision(

            action=action,

            confidence=confidence,

            score=score,

            reasons=reasons,

            bullish_factors=factors.bullish_factors,

            bearish_factors=factors.bearish_factors,

            neutral_factors=factors.neutral_factors,

        )