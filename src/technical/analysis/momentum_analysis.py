"""
Momentum Analysis

RSI
ADX
"""

from src.technical.models.momentum_analysis_result import (
    MomentumAnalysisResult,
)


class MomentumAnalysis:

    def analyze(
        self,
        rsi: float,
        adx: float,
    ) -> MomentumAnalysisResult:

        reasons = []

        confidence = 60
        score = 50
        momentum = "NEUTRAL"

        # ---------------------------------------------
        # Strong Bullish Momentum
        # ---------------------------------------------

        if 55 <= rsi <= 70 and adx >= 25:

            momentum = "STRONG_BULLISH"

            confidence = 90

            score = 90

            reasons.append(
                "RSI healthy with strong ADX."
            )

        # ---------------------------------------------
        # Bullish
        # ---------------------------------------------

        elif rsi > 50:

            momentum = "BULLISH"

            confidence = 75

            score = 75

            reasons.append(
                "RSI above 50."
            )

        # ---------------------------------------------
        # Strong Bearish
        # ---------------------------------------------

        elif 30 <= rsi <= 45 and adx >= 25:

            momentum = "STRONG_BEARISH"

            confidence = 90

            score = 10

            reasons.append(
                "RSI weak with strong ADX."
            )

        # ---------------------------------------------
        # Bearish
        # ---------------------------------------------

        elif rsi < 50:

            momentum = "BEARISH"

            confidence = 75

            score = 25

            reasons.append(
                "RSI below 50."
            )

        # ---------------------------------------------
        # Overbought
        # ---------------------------------------------

        if rsi >= 70:

            reasons.append(
                "Overbought zone."
            )

        # ---------------------------------------------
        # Oversold
        # ---------------------------------------------

        if rsi <= 30:

            reasons.append(
                "Oversold zone."
            )

        # ---------------------------------------------
        # Weak Trend
        # ---------------------------------------------

        if adx < 20:

            reasons.append(
                "Weak trend."
            )

        return MomentumAnalysisResult(

            momentum=momentum,

            confidence=confidence,

            score=score,

            rsi=rsi,

            adx=adx,

            reasons=reasons,
        )