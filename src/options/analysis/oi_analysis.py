"""
Open Interest Analysis
"""

from src.options.models.oi_analysis_result import OIAnalysisResult
from src.options.models.option_chain import OptionChain


class OIAnalysis:
    """
    Analyze Open Interest to determine support and resistance.
    """

    def analyze(self, chain: OptionChain) -> OIAnalysisResult:

        highest_call = None
        highest_put = None

        highest_call_oi = 0
        highest_put_oi = 0

        for call in chain.calls:

            if call.open_interest > highest_call_oi:

                highest_call_oi = call.open_interest
                highest_call = call.strike

        for put in chain.puts:

            if put.open_interest > highest_put_oi:

                highest_put_oi = put.open_interest
                highest_put = put.strike

        return OIAnalysisResult(

            call_resistance=highest_call,

            put_support=highest_put,

            highest_call_oi=highest_call_oi,

            highest_put_oi=highest_put_oi

        )