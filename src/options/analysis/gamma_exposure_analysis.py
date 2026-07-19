"""
Gamma Exposure Analysis
"""

from src.options.models.gamma_exposure_result import (
    GammaExposureResult,
)


class GammaExposureAnalysis:
    """
    Analyze aggregate dealer gamma exposure.
    """

    def analyze(
        self,
        call_gamma: float,
        put_gamma: float,
        gamma_flip: float | None = None,
    ) -> GammaExposureResult:

        reasons = []

        net_gamma = call_gamma - put_gamma

        if net_gamma >= 0:

            status = "POSITIVE_GAMMA"

            confidence = 90

            score = 90

            reasons.append(
                "Dealers likely dampen volatility."
            )

        else:

            status = "NEGATIVE_GAMMA"

            confidence = 90

            score = 20

            reasons.append(
                "Dealers may amplify directional moves."
            )

        if gamma_flip is not None:

            reasons.append(
                f"Gamma flip level: {gamma_flip:.2f}"
            )

        return GammaExposureResult(

            net_gamma=round(net_gamma, 2),

            gamma_flip=gamma_flip,

            status=status,

            confidence=confidence,

            score=score,

            reasons=reasons,
        )