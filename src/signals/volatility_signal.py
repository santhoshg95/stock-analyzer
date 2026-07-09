"""
Volatility Signal Engine

Evaluates whether the stock volatility is suitable
for swing trading using ATR percentage.
"""

import pandas as pd

from src.signals.base_signal import Signal


class VolatilitySignal:

    @staticmethod
    def generate(df: pd.DataFrame) -> Signal:

        latest = df.iloc[-1]

        close = float(latest["Close"])

        atr = float(latest["ATR"])

        atr_percent = (atr / close) * 100

        # --------------------------------------------------
        # ATR Percentage Analysis
        # --------------------------------------------------

        if atr_percent <= 1.5:

            direction = "LOW VOLATILITY"

            strength = 90

            confidence = 90

        elif atr_percent <= 3:

            direction = "HEALTHY VOLATILITY"

            strength = 80

            confidence = 85

        elif atr_percent <= 5:

            direction = "HIGH VOLATILITY"

            strength = 50

            confidence = 75

        else:

            direction = "EXTREME VOLATILITY"

            strength = 20

            confidence = 90

        return Signal(

            name="Volatility",

            direction=direction,

            strength=strength,

            confidence=confidence,

            reason=(
                f"ATR={atr:.2f}, "
                f"ATR%={atr_percent:.2f}%"
            )

        )