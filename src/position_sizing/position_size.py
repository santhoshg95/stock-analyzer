"""
Professional Position Sizing Engine

Calculates executable position size using:

1. Risk Management
2. Capital Management
"""

class PositionSizingEngine:

    @staticmethod
    def calculate(

        capital,

        risk_percent,

        entry,

        stop_loss

    ):

        if (
            entry is None
            or stop_loss is None
            or entry <= 0
            or stop_loss <= 0
        ):

            return {

                "quantity": 0,

                "capital_used": 0,

                "risk_amount": 0,

                "risk_per_share": 0,

                "quantity_risk": 0,

                "quantity_capital": 0

            }

        # ----------------------------------------
        # Risk Amount
        # ----------------------------------------

        risk_amount = capital * (risk_percent / 100)

        risk_per_share = abs(entry - stop_loss)

        if risk_per_share == 0:

            quantity_risk = 0

        else:

            quantity_risk = int(risk_amount / risk_per_share)

        # ----------------------------------------
        # Capital Based Quantity
        # ----------------------------------------

        quantity_capital = int(capital / entry)

        # ----------------------------------------
        # Final Quantity
        # ----------------------------------------

        quantity = min(

            quantity_risk,

            quantity_capital

        )

        capital_used = quantity * entry

        actual_risk = quantity * risk_per_share

        return {

            "quantity": quantity,

            "quantity_risk": quantity_risk,

            "quantity_capital": quantity_capital,

            "capital_used": round(capital_used, 2),

            "risk_amount": round(risk_amount, 2),

            "actual_risk": round(actual_risk, 2),

            "risk_per_share": round(risk_per_share, 2)

        }
