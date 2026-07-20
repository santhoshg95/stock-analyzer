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
        direction: str | None = None,
    ) -> str:

        direction = (direction or "NEUTRAL").upper().replace("_", " ")
        if "BULLISH" in direction:
            # Premium-selling is the primary bullish playbook.  Defined risk
            # is preferred when IV is rich; otherwise reserve assignment cash.
            return "Bull Put Spread" if iv.status in ("HIGH", "VERY_HIGH") else "Cash Secured Put"
        if "BEARISH" in direction:
            return "Bear Call Spread" if iv.status in ("HIGH", "VERY_HIGH") else "Bear Put Spread"

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
