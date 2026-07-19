"""
Volume Analysis

Uses Relative Volume (RVOL).
"""

from src.technical.models.volume_analysis_result import (
    VolumeAnalysisResult,
)


class VolumeAnalysis:

    def analyze(
        self,
        current_volume: float,
        average_volume: float,
    ) -> VolumeAnalysisResult:

        reasons = []

        if average_volume <= 0:
            average_volume = 1

        rvol = current_volume / average_volume

        confidence = 70
        score = 50
        status = "NORMAL"

        # -------------------------------------------------

        if rvol >= 2:

            status = "VOLUME_BREAKOUT"

            confidence = 95

            score = 95

            reasons.append(
                "Volume more than 2x average."
            )

        elif rvol >= 1.5:

            status = "HIGH_VOLUME"

            confidence = 85

            score = 80

            reasons.append(
                "High participation."
            )

        elif rvol >= 0.8:

            status = "NORMAL_VOLUME"

            confidence = 75

            score = 65

            reasons.append(
                "Normal trading activity."
            )

        else:

            status = "LOW_VOLUME"

            confidence = 70

            score = 30

            reasons.append(
                "Weak participation."
            )

        return VolumeAnalysisResult(

            status=status,

            confidence=confidence,

            score=score,

            current_volume=current_volume,

            average_volume=average_volume,

            relative_volume=round(rvol,2),

            reasons=reasons,
        )