"""
Momentum Signal Engine

Uses RSI and MACD to determine momentum strength.
"""

import pandas as pd

from src.signals.base_signal import Signal


class MomentumSignal:

    @staticmethod
    def generate(df: pd.DataFrame) -> Signal:

        latest = df.iloc[-1]

        rsi = float(latest["RSI"])

        macd = float(latest["MACD"])

        macd_signal = float(latest["MACD_SIGNAL"])

        score = 0

        reasons = []

        # --------------------------------------------------
        # RSI Analysis
        # --------------------------------------------------

        if 55 <= rsi <= 70:

            score += 50

            reasons.append("Healthy RSI")

        elif 45 <= rsi < 55:

            score += 35

            reasons.append("Neutral RSI")

        elif 30 <= rsi < 45:

            score += 20

            reasons.append("Weak RSI")

        elif rsi < 30:

            score += 40

            reasons.append("Oversold (Possible Reversal)")

        else:

            score += 10

            reasons.append("Overbought")

        # --------------------------------------------------
        # MACD Analysis
        # --------------------------------------------------

        if macd > macd_signal:

            score += 50

            reasons.append("Bullish MACD Crossover")

        else:

            reasons.append("Bearish MACD Crossover")

        # --------------------------------------------------
        # Final Direction
        # --------------------------------------------------

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

            name="Momentum",

            direction=direction,

            strength=score,

            confidence=confidence,

            reason=", ".join(reasons)

        )