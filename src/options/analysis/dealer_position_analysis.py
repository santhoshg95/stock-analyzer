"""
Dealer Position Analysis
"""

from src.options.models.dealer_position_result import (
    DealerPositionResult,
)


class DealerPositionAnalysis:
    """
    Infer dealer positioning from option chain data.
    """

    def analyze(
        self,
        support_strike: float | None,
        resistance_strike: float | None,
        call_writing: float,
        put_writing: float,
    ) -> DealerPositionResult:

        reasons = []

        if put_writing > call_writing:

            bias = "BULLISH"

            confidence = 90

            score = 90

            reasons.append(
                "Put writing exceeds call writing."
            )

        elif call_writing > put_writing:

            bias = "BEARISH"

            confidence = 90

            score = 20

            reasons.append(
                "Call writing exceeds put writing."
            )

        else:

            bias = "NEUTRAL"

            confidence = 70

            score = 50

            reasons.append(
                "Balanced positioning."
            )

        if support_strike is not None:

            reasons.append(
                f"Support near {support_strike:.2f}"
            )

        if resistance_strike is not None:

            reasons.append(
                f"Resistance near {resistance_strike:.2f}"
            )

        return DealerPositionResult(

            market_bias=bias,

            support_strike=support_strike,

            resistance_strike=resistance_strike,

            confidence=confidence,

            score=score,

            reasons=reasons,
        )