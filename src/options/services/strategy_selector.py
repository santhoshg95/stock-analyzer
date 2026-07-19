"""
Option Strategy Selector
"""

from src.options.models.greeks_analysis_result import GreeksAnalysisResult
from src.options.models.iv_analysis_result import IVAnalysisResult
from src.options.models.pcr_analysis_result import PCRAnalysisResult


class OptionStrategySelector:
    """
    Chooses the best option strategy.
    """

    def select(
        self,
        pcr: PCRAnalysisResult,
        iv: IVAnalysisResult,
        greeks: GreeksAnalysisResult,
    ) -> str:

        if (

            pcr.sentiment == "BULLISH"

            and

            iv.status in ("HIGH", "VERY_HIGH")

        ):

            return "Bull Put Spread"

        if (

            pcr.sentiment == "BEARISH"

            and

            iv.status in ("HIGH", "VERY_HIGH")

        ):

            return "Bear Call Spread"

        if (

            iv.status == "VERY_HIGH"

        ):

            return "Iron Condor"

        return "Wait"