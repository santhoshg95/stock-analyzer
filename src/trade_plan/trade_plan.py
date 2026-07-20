"""
Trade Plan Engine

Generates a complete trade plan using
support, resistance and risk-reward.
"""

from src.models.trade_plan import TradePlan


class TradePlanEngine:

    @staticmethod
    def generate(entry_report):

        current_price = entry_report["current_price"]

        support = entry_report["support"]

        resistance = entry_report["resistance"]

        quality = entry_report["quality"]

        # ----------------------------------------------------

        if support is None or resistance is None:

            return TradePlan(

                entry=0.0,

                stop_loss=0.0,

                target1=0.0,

                target2=0.0,

                target3=0.0,

                risk=0.0,

                reward=0.0,

                risk_reward=0.0,

                quality="UNKNOWN"

            )

        # ----------------------------------------------------

        entry = current_price

        atr = max(float(entry_report.get("atr") or 0), 0)
        minimum_distance = max(abs(entry - support), atr * 0.75, entry * 0.0075)
        stop_loss = entry - minimum_distance
        risk = abs(entry - stop_loss)
        target1 = entry + risk * 1.5
        if resistance > entry:
            target1 = min(resistance, target1)
        target2 = entry + risk * 2
        target3 = entry + risk * 3
        reward = target1 - entry
        risk_reward = reward / risk if risk > 0 else 0
        quality = "GOOD" if risk_reward >= 2 else "AVERAGE" if risk_reward >= 1.5 else "POOR"

        # ----------------------------------------------------

        return TradePlan(

            entry=round(entry, 2),

            stop_loss=round(stop_loss, 2),

            target1=round(target1, 2),

            target2=round(target2, 2),

            target3=round(target3, 2),

            risk=round(risk, 2),

            reward=round(reward, 2),

            risk_reward=round(risk_reward, 2),

            quality=quality

        )
