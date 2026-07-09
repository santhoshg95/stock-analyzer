"""
Breakout Detector

Detects high-quality bullish breakouts using
trend, volume, RSI and resistance.
"""

from src.market_structure.support_resistance import SupportResistanceEngine


class BreakoutDetector:

    @staticmethod
    def analyze(df):

        latest = df.iloc[-1]

        close = float(latest["Close"])

        rsi = float(latest["RSI"])

        ema20 = float(latest["EMA20"])
        ema50 = float(latest["EMA50"])
        ema200 = float(latest["EMA200"])

        rvol = float(latest["RVOL"])

        macd = float(latest["MACD"])

        signal = float(latest["MACD_SIGNAL"])

        levels = SupportResistanceEngine.calculate(df)

        resistance = levels["resistance"]

        # ----------------------------------------
        # Individual Conditions
        # ----------------------------------------

        conditions = {

            "Above Resistance": (
                resistance is not None and close > resistance
            ),

            "Bullish Trend": (
                close > ema20 > ema50 > ema200
            ),

            "High Volume": (
                rvol >= 1.5
            ),

            "Healthy RSI": (
                rsi < 75
            ),

            "Bullish MACD": (
                macd > signal
            )

        }

        passed = sum(conditions.values())

        confirmed = passed == len(conditions)

        return {

            "confirmed": confirmed,

            "score": passed,

            "total_conditions": len(conditions),

            "conditions": conditions,

            "resistance": resistance

        }