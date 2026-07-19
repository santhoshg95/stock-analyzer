"""
Market Narrative Engine
"""

from src.ai.models.market_narrative import MarketNarrative


class MarketNarrativeEngine:
    """
    Generate a human-readable explanation of the market.
    """

    def generate(
        self,
        trend: str,
        regime: str,
        iv_rank: float,
        dealer_bias: str,
        gamma_status: str,
    ) -> MarketNarrative:

        points = []

        points.append(f"Trend: {trend}")
        points.append(f"Market Regime: {regime}")
        points.append(f"IV Rank: {iv_rank:.2f}")
        points.append(f"Dealer Bias: {dealer_bias}")
        points.append(f"Gamma: {gamma_status}")

        summary = (
            f"The market is currently in a {regime.lower()} "
            f"environment with a {trend.lower()} bias."
        )

        if regime == "RANGE_BOUND":
            behavior = (
                "Expect prices to remain within defined support "
                "and resistance zones."
            )
        elif regime == "TRENDING_BULL":
            behavior = (
                "Expect continued upward momentum with controlled pullbacks."
            )
        elif regime == "TRENDING_BEAR":
            behavior = (
                "Expect continued downward pressure with relief rallies."
            )
        elif regime == "EVENT_DRIVEN":
            behavior = (
                "Expect higher uncertainty and larger intraday moves."
            )
        else:
            behavior = (
                "Expect mixed price action until a clearer regime develops."
            )

        return MarketNarrative(
            summary=summary,
            expected_behavior=behavior,
            confidence=90.0,
            key_points=points,
        )