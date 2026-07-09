"""
Adaptive Weight Engine

Adjusts factor weights according to market conditions.
"""


class AdaptiveWeightEngine:

    @staticmethod
    def get_weights(context):

        market = context.market

        # Default weights
        weights = {

            "MARKET": 0.20,
            "TECHNICAL": 0.30,
            "SECTOR": 0.15,
            "NEWS": 0.20,
            "OPTION": 0.15

        }

        # Example adaptation

        if market.status == "BEARISH":

            weights["MARKET"] = 0.30
            weights["TECHNICAL"] = 0.25

        elif market.status == "BULLISH":

            weights["TECHNICAL"] = 0.35
            weights["MARKET"] = 0.15

        return weights