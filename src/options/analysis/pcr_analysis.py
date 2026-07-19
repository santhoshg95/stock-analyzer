"""
Put Call Ratio Analysis
"""

from src.options.models.option_chain import OptionChain
from src.options.models.pcr_analysis_result import PCRAnalysisResult


class PCRAnalysis:
    """
    Calculate Put Call Ratio.
    """

    def analyze(self, chain: OptionChain) -> PCRAnalysisResult:

        total_call_oi = sum(

            call.open_interest

            for call in chain.calls

        )

        total_put_oi = sum(

            put.open_interest

            for put in chain.puts

        )

        if total_call_oi == 0:

            pcr = 0

        else:

            pcr = total_put_oi / total_call_oi

        if pcr > 1.2:

            sentiment = "BULLISH"

        elif pcr < 0.8:

            sentiment = "BEARISH"

        else:

            sentiment = "NEUTRAL"

        return PCRAnalysisResult(

            pcr=round(

                pcr,

                2

            ),

            sentiment=sentiment,

            total_call_oi=total_call_oi,

            total_put_oi=total_put_oi

        )