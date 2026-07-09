"""
Stock Analysis Engine
"""

import pandas as pd


class StockAnalyzer:

    @staticmethod
    def analyze(symbol: str, df: pd.DataFrame):

        latest = df.iloc[-1]

        close = float(latest["Close"])
        ema20 = float(latest["EMA20"])
        ema50 = float(latest["EMA50"])
        ema200 = float(latest["EMA200"])
        rsi = float(latest["RSI"])

        above20 = close > ema20
        above50 = close > ema50
        above200 = close > ema200

        if above20 and above50 and above200:
            trend = "STRONG BULLISH"
        elif not above20 and not above50 and not above200:
            trend = "STRONG BEARISH"
        elif above200:
            trend = "LONG TERM BULLISH"
        else:
            trend = "SIDEWAYS"

        if rsi >= 70:
            rsi_signal = "OVERBOUGHT"
        elif rsi <= 30:
            rsi_signal = "OVERSOLD"
        elif rsi >= 50:
            rsi_signal = "BULLISH MOMENTUM"
        else:
            rsi_signal = "BEARISH MOMENTUM"

        print()
        print("=" * 70)
        print(symbol)
        print("=" * 70)

        print(f"Current Price : ₹{close:.2f}")

        print("\nMoving Averages")
        print("-" * 70)

        print(f"EMA20  : ₹{ema20:.2f}")
        print(f"EMA50  : ₹{ema50:.2f}")
        print(f"EMA200 : ₹{ema200:.2f}")

        print("\nTrend Analysis")
        print("-" * 70)

        print(f"Price Above EMA20  : {'YES' if above20 else 'NO'}")
        print(f"Price Above EMA50  : {'YES' if above50 else 'NO'}")
        print(f"Price Above EMA200 : {'YES' if above200 else 'NO'}")

        print(f"Overall Trend      : {trend}")

        print("\nMomentum")
        print("-" * 70)

        print(f"RSI : {rsi:.2f}")
        print(f"Signal : {rsi_signal}")

        print("=" * 70)