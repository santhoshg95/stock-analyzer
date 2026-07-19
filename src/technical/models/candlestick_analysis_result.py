"""
Candlestick Analysis

Supports:

- Bullish Engulfing
- Bearish Engulfing
- Hammer
- Shooting Star
- Morning Star
- Evening Star
"""

from src.technical.models.candlestick_analysis_result import (
    CandlestickAnalysisResult,
)
from src.technical.models.candlestick_pattern import (
    CandlestickPattern,
)


class CandlestickAnalysis:
    """
    Detect high probability candlestick patterns.
    """

    def analyze(
        self,
        candles: list[dict],
    ) -> CandlestickAnalysisResult:

        if len(candles) < 3:

            return CandlestickAnalysisResult(
                pattern=None,
                score=50,
                confidence=0,
                reasons=["Not enough candle data."],
            )

        #
        # Placeholder
        #
        # Pattern detection methods will be implemented
        # individually:
        #
        # detect_bullish_engulfing()
        # detect_bearish_engulfing()
        # detect_hammer()
        # detect_shooting_star()
        # detect_morning_star()
        # detect_evening_star()
        #

        return CandlestickAnalysisResult(
            pattern=None,
            score=50,
            confidence=0,
            reasons=["No high-confidence pattern detected."],
        )