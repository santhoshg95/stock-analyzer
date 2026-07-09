"""
Trade Plan Engine

Generates a practical trade plan using
current price, support, resistance and
risk/reward.
"""


class TradePlanEngine:

    @staticmethod
    def generate(entry_report):

        current_price = entry_report["current_price"]

        support = entry_report["support"]

        resistance = entry_report["resistance"]

        risk = entry_report["risk"]

        reward = entry_report["reward"]

        rr = entry_report["risk_reward"]

        quality = entry_report["quality"]

        if support is None or resistance is None:

            return {

                "entry": None,

                "stop_loss": None,

                "target1": None,

                "target2": None,

                "risk_reward": None,

                "quality": "UNKNOWN"

            }

        # ---------------------------------------
        # Entry
        # ---------------------------------------

        entry = current_price

        # ---------------------------------------
        # Stop Loss
        # ---------------------------------------

        stop_loss = support

        # ---------------------------------------
        # Targets
        # ---------------------------------------

        target1 = resistance

        target2 = resistance + reward

        return {

            "entry": round(entry, 2),

            "stop_loss": round(stop_loss, 2),

            "target1": round(target1, 2),

            "target2": round(target2, 2),

            "risk": round(risk, 2),

            "reward": round(reward, 2),

            "risk_reward": rr,

            "quality": quality

        }