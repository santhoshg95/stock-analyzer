"""
Max Pain Analysis
"""

from src.options.models.max_pain_result import MaxPainResult
from src.options.models.option_chain import OptionChain


class MaxPainAnalysis:

    def analyze(self, chain: OptionChain) -> MaxPainResult:

        strikes = sorted(

            {c.strike for c in chain.calls}

            |

            {p.strike for p in chain.puts}

        )

        if not strikes:

            return MaxPainResult(

                max_pain=None

            )

        payout = {}

        for expiry_price in strikes:

            total = 0

            for call in chain.calls:

                total += max(

                    0,

                    expiry_price - call.strike

                ) * call.open_interest

            for put in chain.puts:

                total += max(

                    0,

                    put.strike - expiry_price

                ) * put.open_interest

            payout[expiry_price] = total

        return MaxPainResult(

            max_pain=min(

                payout,

                key=payout.get

            ),

            payout=payout

        )