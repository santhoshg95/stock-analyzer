"""
Option Confidence Calculator
"""

from src.options.models.greeks_analysis_result import GreeksAnalysisResult
from src.options.models.iv_analysis_result import IVAnalysisResult
from src.options.models.liquidity_analysis_result import LiquidityAnalysisResult
from src.options.models.pcr_analysis_result import PCRAnalysisResult


class OptionConfidenceCalculator:
    """
    Calculates overall confidence for option analysis.
    """

    BASE_CONFIDENCE = 50

    def calculate(
        self,
        pcr: PCRAnalysisResult,
        liquidity: LiquidityAnalysisResult,
        iv: IVAnalysisResult,
        greeks: GreeksAnalysisResult,
    ) -> tuple[int, list[str]]:

        confidence = self.BASE_CONFIDENCE

        reasons = []

        # -------------------------------------------------
        # PCR
        # -------------------------------------------------

        if pcr.sentiment == "BULLISH":

            confidence += 20

            reasons.append(
                "PCR indicates bullish positioning."
            )

        elif pcr.sentiment == "BEARISH":

            confidence -= 20

            reasons.append(
                "PCR indicates bearish positioning."
            )

        else:

            reasons.append(
                "PCR indicates neutral positioning."
            )

        # -------------------------------------------------
        # Liquidity
        # -------------------------------------------------

        confidence += liquidity.confidence // 10

        reasons.extend(
            liquidity.reasons
        )

        # -------------------------------------------------
        # IV
        # -------------------------------------------------

        confidence += iv.confidence // 20

        reasons.extend(
            iv.reasons
        )

        # -------------------------------------------------
        # Greeks
        # -------------------------------------------------

        confidence += greeks.confidence // 20

        reasons.extend(
            greeks.reasons
        )

        confidence = max(
            0,
            min(confidence, 100)
        )

        return confidence, reasons