"""
Risk Reward Engine

Uses support and resistance levels to calculate
risk, reward and risk-reward ratio.
"""

class RiskRewardEngine:

    @staticmethod
    def calculate(
        current_price,
        support,
        resistance
    ):

        if support is None or resistance is None:

            return {

                "risk": None,

                "reward": None,

                "risk_reward": None,

                "quality": "UNKNOWN"

            }

        risk = current_price - support

        reward = resistance - current_price

        if risk <= 0:

            ratio = None

        else:

            ratio = reward / risk

        # -------------------------------------

        if ratio is None:

            quality = "UNKNOWN"

        elif ratio >= 3:

            quality = "EXCELLENT"

        elif ratio >= 2:

            quality = "GOOD"

        elif ratio >= 1:

            quality = "AVERAGE"

        else:

            quality = "POOR"

        return {

            "risk": round(risk,2),

            "reward": round(reward,2),

            "risk_reward": round(ratio,2) if ratio else None,

            "quality": quality

        }