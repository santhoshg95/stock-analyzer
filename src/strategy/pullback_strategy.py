"""
Pullback Strategy
"""

from src.strategy.base_strategy import BaseStrategy


class PullbackStrategy(BaseStrategy):

    def evaluate(self, report):

        analysis = report["analysis"]

        entry = report["entry"]

        score = analysis.score

        # ------------------------------------------------

        if score < 60:

            return None

        if entry["risk_reward"] < 2:

            return None

        if entry["support_distance"] > 2:

            return None

        return {

            "strategy": "PULLBACK BUY",

            "confidence": 90,

            "reason":

                "Near support with attractive risk/reward."

        }