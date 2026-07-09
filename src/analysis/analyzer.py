"""
Stock Analysis Engine

Coordinates:
1. Signal Pipeline
2. Score Engine
3. StockAnalysis Model
"""

import pandas as pd

from src.models.stock_analysis import StockAnalysis
from src.scoring.score_engine import ScoreEngine
from src.signals.pipeline import SignalPipeline


class StockAnalyzer:

    @staticmethod
    def analyze(symbol: str, df: pd.DataFrame) -> StockAnalysis:

        latest = df.iloc[-1]

        # ---------------------------------------------------------
        # Generate Signals
        # ---------------------------------------------------------

        signals = SignalPipeline.run(df)

        trend_signal = next(
            signal for signal in signals
            if signal.name == "Trend"
        )

        momentum_signal = next(
            signal for signal in signals
            if signal.name == "Momentum"
        )

        # ---------------------------------------------------------
        # Score
        # ---------------------------------------------------------

        score = ScoreEngine.calculate(signals)

        # ---------------------------------------------------------
        # Basic Market Data
        # ---------------------------------------------------------

        close = float(latest["Close"])

        ema20 = float(latest["EMA20"])
        ema50 = float(latest["EMA50"])
        ema200 = float(latest["EMA200"])

        rsi = float(latest["RSI"])

        macd = float(latest["MACD"])
        macd_signal_line = float(latest["MACD_SIGNAL"])
        macd_histogram = float(latest["MACD_HISTOGRAM"])

        atr = float(latest["ATR"])

        volume = int(latest["Volume"])
        average_volume = float(latest["AVG_VOLUME"])
        relative_volume = float(latest["RVOL"])
        volume_signal = latest["VOLUME_SIGNAL"]

        expected_low = close - atr
        expected_high = close + atr

        # ---------------------------------------------------------
        # Build Analysis Object
        # ---------------------------------------------------------

        return StockAnalysis(

            symbol=symbol,

            current_price=close,

            ema20=ema20,
            ema50=ema50,
            ema200=ema200,

            trend=trend_signal.direction,

            rsi=rsi,
            rsi_signal=momentum_signal.direction,

            macd=macd,
            macd_signal_line=macd_signal_line,
            macd_histogram=macd_histogram,
            macd_signal=momentum_signal.reason,

            atr=atr,

            expected_low=expected_low,
            expected_high=expected_high,

            volume=volume,
            average_volume=average_volume,
            relative_volume=relative_volume,
            volume_signal=volume_signal,

            score=score["score"],
            max_score=score["max_score"],
            recommendation=score["recommendation"]

        )