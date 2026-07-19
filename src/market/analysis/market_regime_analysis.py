"""
Market Regime Analysis
"""

from src.market.models.market_regime import MarketRegime


class MarketRegimeAnalysis:

    def analyze(
        self,
        trend: str,
        volatility: str,
        gamma: str,
        news_impact: str,
    ) -> MarketRegime:

        reasons = []

        #
        # Event Driven
        #

        if news_impact == "HIGH":

            return MarketRegime(

                regime="EVENT_DRIVEN",

                confidence=98,

                reasons=[
                    "High impact news detected."
                ],
            )

        #
        # Bull Trend
        #

        if (
            trend == "STRONG_BULLISH"
            and gamma == "NEGATIVE_GAMMA"
        ):

            return MarketRegime(

                regime="TRENDING_BULL",

                confidence=95,

                reasons=[
                    "Strong bullish trend with directional gamma."
                ],
            )

        #
        # Bear Trend
        #

        if (
            trend == "STRONG_BEARISH"
            and gamma == "NEGATIVE_GAMMA"
        ):

            return MarketRegime(

                regime="TRENDING_BEAR",

                confidence=95,

                reasons=[
                    "Strong bearish trend."
                ],
            )

        #
        # Range
        #

        if gamma == "POSITIVE_GAMMA":

            return MarketRegime(

                regime="RANGE_BOUND",

                confidence=90,

                reasons=[
                    "Positive gamma usually stabilizes price."
                ],
            )

        #
        # High Volatility
        #

        if volatility == "EXTREME":

            return MarketRegime(

                regime="HIGH_VOLATILITY",

                confidence=90,

                reasons=[
                    "ATR indicates extreme volatility."
                ],
            )

        return MarketRegime(

            regime="NORMAL",

            confidence=70,

            reasons=[
                "No dominant regime detected."
            ],
        )