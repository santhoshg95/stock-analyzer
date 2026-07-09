"""
Support Signal Engine

Determines whether the current price is near a support
or resistance level.
"""

import pandas as pd

from src.market_structure.support_resistance import SupportResistanceEngine
from src.signals.base_signal import Signal


class SupportSignal:

    @staticmethod
    def generate(df: pd.DataFrame) -> Signal:

        levels = SupportResistanceEngine.calculate(df)

        support = levels["support"]
        resistance = levels["resistance"]

        support_distance = levels["support_distance"]
        resistance_distance = levels["resistance_distance"]

        # ------------------------------------------
        # No Levels Found
        # ------------------------------------------

        if support is None or resistance is None:

            return Signal(

                name="Support",

                direction="UNKNOWN",

                strength=40,

                confidence=40,

                reason="Support/Resistance could not be determined."

            )

        # ------------------------------------------
        # Near Support
        # ------------------------------------------

        if support_distance <= 2:

            return Signal(

                name="Support",

                direction="NEAR SUPPORT",

                strength=90,

                confidence=90,

                reason=(
                    f"Support ₹{support:.2f} "
                    f"({support_distance:.2f}% away)"
                )

            )

        # ------------------------------------------
        # Near Resistance
        # ------------------------------------------

        if resistance_distance <= 2:

            return Signal(

                name="Support",

                direction="NEAR RESISTANCE",

                strength=20,

                confidence=90,

                reason=(
                    f"Resistance ₹{resistance:.2f} "
                    f"({resistance_distance:.2f}% away)"
                )

            )

        # ------------------------------------------
        # Between Levels
        # ------------------------------------------

        return Signal(

            name="Support",

            direction="MID RANGE",

            strength=60,

            confidence=75,

            reason=(
                f"Support ₹{support:.2f}, "
                f"Resistance ₹{resistance:.2f}"
            )

        )