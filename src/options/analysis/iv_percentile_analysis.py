"""
IV Percentile Analysis
"""

from src.options.models.iv_percentile_result import (
    IVPercentileResult,
)


class IVPercentileAnalysis:

    def analyze(
        self,
        current_iv: float,
        historical_iv: list[float],
    ) -> IVPercentileResult:

        if not historical_iv:

            return IVPercentileResult(

                percentile=0,

                status="UNKNOWN",

                confidence=0,

                score=50,

                reasons=["Historical IV unavailable."],
            )

        lower = sum(
            iv < current_iv
            for iv in historical_iv
        )

        percentile = (
            lower / len(historical_iv)
        ) * 100

        percentile = round(percentile,2)

        reasons = []

        if percentile >= 80:

            status = "VERY_HIGH"

            confidence = 95

            score = 95

            reasons.append(
                "IV higher than most historical observations."
            )

        elif percentile >= 60:

            status = "HIGH"

            confidence = 85

            score = 80

            reasons.append(
                "IV above historical average."
            )

        elif percentile >= 40:

            status = "NORMAL"

            confidence = 75

            score = 60

            reasons.append(
                "IV near historical average."
            )

        else:

            status = "LOW"

            confidence = 80

            score = 25

            reasons.append(
                "IV below historical average."
            )

        return IVPercentileResult(

            percentile=percentile,

            status=status,

            confidence=confidence,

            score=score,

            reasons=reasons,
        )