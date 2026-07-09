"""
Trend Signal Engine

Converts EMA values into a meaningful trend signal.
"""

import pandas as pd

from src.signals.base_signal import Signal


class TrendSignal:

    @staticmethod
    def generate(df: pd.DataFrame) -> Signal:

        latest = df.iloc[-1]

        close = float(latest["Close"])

        ema20 = float(latest["EMA20"])
        ema50 = float(latest["EMA50"])
        ema200 = float(latest["EMA200"])

        score = 0
        reasons = []

        # -------------------------------------------------
        # Price vs EMA20
        # -------------------------------------------------

        if close > ema20:
            score += 20
            reasons.append("Price above EMA20")
        else:
            reasons.append("Price below EMA20")

        # -------------------------------------------------
        # Price vs EMA50
        # -------------------------------------------------

        if close > ema50:
            score += 30
            reasons.append("Price above EMA50")
        else:
            reasons.append("Price below EMA50")

        # -------------------------------------------------
        # Price vs EMA200
        # -------------------------------------------------

        if close > ema200:
            score += 50
            reasons.append("Price above EMA200")
        else:
            reasons.append("Price below EMA200")

        # -------------------------------------------------
        # Direction
        # -------------------------------------------------

        if score >= 80:
            direction = "STRONG BULLISH"

        elif score >= 60:
            direction = "BULLISH"

        elif score >= 40:
            direction = "NEUTRAL"

        elif score >= 20:
            direction = "BEARISH"

        else:
            direction = "STRONG BEARISH"

        confidence = score

        return Signal(

            name="Trend",

            direction=direction,

            strength=score,

            confidence=confidence,

            reason=", ".join(reasons)

        )