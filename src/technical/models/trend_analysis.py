"""
Trend Analysis

EMA20
EMA50
EMA200
"""

from src.technical.models.trend_analysis_result import (
    TrendAnalysisResult,
)


class TrendAnalysis:

    def analyze(
        self,
        ema20: float,
        ema50: float,
        ema200: float,
    ) -> TrendAnalysisResult:

        reasons = []

        confidence = 50

        score = 50

        # -------------------------------------------------
        # Strong Bullish
        # -------------------------------------------------

        if ema20 > ema50 > ema200:

            trend = "STRONG_BULLISH"

            confidence = 95

            score = 95

            reasons.append(
                "EMA20 > EMA50 > EMA200"
            )

        # -------------------------------------------------
        # Bullish
        # -------------------------------------------------

        elif ema20 > ema50:

            trend = "BULLISH"

            confidence = 80

            score = 80

            reasons.append(
                "EMA20 above EMA50"
            )

        # -------------------------------------------------
        # Strong Bearish
        # -------------------------------------------------

        elif ema20 < ema50 < ema200:

            trend = "STRONG_BEARISH"

            confidence = 95

            score = 5

            reasons.append(
                "EMA20 < EMA50 < EMA200"
            )

        # -------------------------------------------------
        # Bearish
        # -------------------------------------------------

        elif ema20 < ema50:

            trend = "BEARISH"

            confidence = 80

            score = 20

            reasons.append(
                "EMA20 below EMA50"
            )

        else:

            trend = "SIDEWAYS"

            confidence = 55

            score = 50

            reasons.append(
                "Mixed EMA alignment"
            )

        return TrendAnalysisResult(

            trend=trend,

            confidence=confidence,

            score=score,

            ema20=ema20,

            ema50=ema50,

            ema200=ema200,

            reasons=reasons,
        )