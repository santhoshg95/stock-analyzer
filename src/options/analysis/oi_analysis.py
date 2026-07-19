"""
Open Interest Analysis
"""

from src.options.models.option_chain import OptionChain


class OIAnalysis:

    def analyze(self, chain: OptionChain):

        highest_call = max(
            chain.calls,
            key=lambda x: x.open_interest,
            default=None
        )

        highest_put = max(
            chain.puts,
            key=lambda x: x.open_interest,
            default=None
        )

        return {

            "highest_call_oi": highest_call,

            "highest_put_oi": highest_put,

            "call_resistance":
                highest_call.strike if highest_call else None,

            "put_support":
                highest_put.strike if highest_put else None,

        }