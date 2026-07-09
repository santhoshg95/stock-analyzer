"""
Volume Signal Engine

Evaluates participation using Relative Volume (RVOL).
"""

import pandas as pd

from src.signals.base_signal import Signal


class VolumeSignal:
    """
    Generates a volume-based trading signal.
    """

    @staticmethod
    def generate(df: pd.DataFrame) -> Signal:

        latest = df.iloc[-1]

        rvol = float(latest["RVOL"])

        volume = int(latest["Volume"])

        avg_volume = float(latest["AVG_VOLUME"])

        # -------------------------------------------------
        # Score RVOL
        # -------------------------------------------------

        if rvol >= 2.0:

            direction = "VERY HIGH PARTICIPATION"
            strength = 100
            confidence = 95

        elif rvol >= 1.5:

            direction = "HIGH PARTICIPATION"
            strength = 85
            confidence = 90

        elif rvol >= 1.0:

            direction = "NORMAL PARTICIPATION"
            strength = 65
            confidence = 80

        elif rvol >= 0.75:

            direction = "LOW PARTICIPATION"
            strength = 40
            confidence = 70

        else:

            direction = "VERY LOW PARTICIPATION"
            strength = 15
            confidence = 60

        return Signal(

            name="Volume",

            direction=direction,

            strength=strength,

            confidence=confidence,

            reason=(
                f"Today's Volume={volume:,}, "
                f"20 Day Avg={avg_volume:,.0f}, "
                f"RVOL={rvol:.2f}"
            )

        )