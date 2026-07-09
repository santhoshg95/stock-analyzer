"""
Decision Engine

This is the brain of the AI Trading Assistant.

Every engine contributes evidence and this class
produces the final trading decision.
"""


class DecisionEngine:

    @staticmethod
    def decide(report: dict):

        analysis = report["analysis"]

        entry = report["entry"]

        breakout = report["breakout"]

        score = analysis.score

        risk_reward = entry["risk_reward"]

        # --------------------------------------------------
        # Rule 1
        # Weak Technical Structure
        # --------------------------------------------------

        if score < 40:

            return {

                "action": "AVOID",

                "confidence": 95,

                "reason": "Overall technical structure is weak."

            }

        # --------------------------------------------------
        # Rule 2
        # Confirmed Breakout
        # --------------------------------------------------

        if breakout["confirmed"]:

            return {

                "action": "BUY",

                "confidence": 95,

                "reason": "Confirmed breakout with strong technical confirmation."

            }

        # --------------------------------------------------
        # Rule 3
        # Good Risk Reward
        # --------------------------------------------------

        if risk_reward is not None and risk_reward >= 2:

            return {

                "action": "BUY ON DIP",

                "confidence": 85,

                "reason": "Good risk-reward setup. Wait for pullback near support."

            }

        # --------------------------------------------------
        # Rule 4
        # Watchlist
        # --------------------------------------------------

        if score >= 60:

            return {

                "action": "WATCH",

                "confidence": 75,

                "reason": "Technically decent stock but no high-probability entry."

            }

        # --------------------------------------------------
        # Default
        # --------------------------------------------------

        return {

            "action": "WAIT",

            "confidence": 70,

            "reason": "Current setup is mixed. Wait for stronger confirmation."

        }