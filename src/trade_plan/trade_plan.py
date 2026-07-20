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

        risk = entry_report["risk"]

        reward = entry_report["reward"]

        risk_reward = entry_report["risk_reward"]

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

        stop_loss = support

        target1 = resistance

        target2 = resistance + reward

        target3 = resistance + (reward * 2)

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
