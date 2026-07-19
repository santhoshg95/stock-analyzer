"""
Option Analysis Builder
"""

from src.options.models.greeks_analysis_result import GreeksAnalysisResult
from src.options.models.iv_analysis_result import IVAnalysisResult
from src.options.models.max_pain_result import MaxPainResult
from src.options.models.oi_analysis_result import OIAnalysisResult
from src.options.models.option_analysis import OptionAnalysis
from src.options.models.pcr_analysis_result import PCRAnalysisResult


class OptionAnalysisBuilder:
    """
    Builds OptionAnalysis.
    """

    def build(
        self,
        confidence: int,
        reasons: list[str],
        strategy: str,
        oi: OIAnalysisResult,
        pcr: PCRAnalysisResult,
        iv: IVAnalysisResult,
        max_pain: MaxPainResult,
    ) -> OptionAnalysis:

        if confidence >= 75:

            status = "STRONG"

        elif confidence >= 60:

            status = "GOOD"

        elif confidence >= 40:

            status = "NEUTRAL"

        else:

            status = "WEAK"

        return OptionAnalysis(

            status=status,

            confidence=confidence,

            score=confidence,

            pcr=pcr.pcr,

            iv_rank=iv.average_iv,

            max_pain=max_pain.max_pain,

            strongest_support=oi.put_support,

            strongest_resistance=oi.call_resistance,

            suggested_strategy=strategy,

            reasons=reasons

        )