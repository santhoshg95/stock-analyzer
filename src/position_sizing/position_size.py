"""
Position Sizing Engine

Calculates position size based on
capital and maximum risk per trade.
"""


class PositionSizingEngine:

    @staticmethod
    def calculate(

        capital,

        risk_percent,

        entry,

        stop_loss

    ):

        if entry is None or stop_loss is None:

            return {

                "quantity": 0,

                "capital_used": 0,

                "risk_amount": 0,

                "risk_per_share": 0

            }

        # -----------------------------------------

        risk_amount = capital * (risk_percent / 100)

        risk_per_share = abs(entry - stop_loss)

        if risk_per_share == 0:

            quantity = 0

        else:

            quantity = int(risk_amount / risk_per_share)

        capital_used = quantity * entry

        return {

            "quantity": quantity,

            "capital_used": round(capital_used, 2),

            "risk_amount": round(risk_amount, 2),

            "risk_per_share": round(risk_per_share, 2)

        }