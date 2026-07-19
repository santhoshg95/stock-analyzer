"""
Volatility Analysis

Uses ATR to measure market volatility.
"""

from src.technical.models.volatility_analysis_result import (
    VolatilityAnalysisResult,
)


class VolatilityAnalysis:

    def analyze(
        self,
        atr: float,
        current_price: float,
    ) -> VolatilityAnalysisResult:

        reasons = []

        atr_percent = (atr / current_price) * 100

        confidence = 70
        score = 50
        volatility = "NORMAL"

        if atr_percent < 1:

            volatility = "LOW"

            confidence = 80

            score = 80

            reasons.append(
                "Low volatility."
            )

        elif atr_percent < 2:

            volatility = "NORMAL"

            confidence = 85

            score = 70

            reasons.append(
                "Healthy volatility."
            )

        elif atr_percent < 3.5:

            volatility = "HIGH"

            confidence = 80

            score = 40

            reasons.append(
                "High volatility."
            )

        else:

            volatility = "EXTREME"

            confidence = 95

            score = 15

            reasons.append(
                "Extreme volatility."
            )

        return VolatilityAnalysisResult(

            volatility=volatility,

            confidence=confidence,

            score=score,

            atr=atr,

            atr_percentage=round(atr_percent,2),

            expected_move=round(atr,2),

            reasons=reasons,
        )