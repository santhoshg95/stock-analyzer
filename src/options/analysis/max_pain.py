"""
Max Pain Analysis
"""

from src.options.models.option_chain import OptionChain


class MaxPainAnalysis:

    def analyze(self, chain: OptionChain):

        strikes = sorted(
            {c.strike for c in chain.calls} |
            {p.strike for p in chain.puts}
        )

        if not strikes:
            return {
                "max_pain": None
            }

        payout = {}

        for expiry_price in strikes:

            total = 0

            # Call writers payout
            for call in chain.calls:

                total += max(
                    0,
                    expiry_price - call.strike
                ) * call.open_interest

            # Put writers payout
            for put in chain.puts:

                total += max(
                    0,
                    put.strike - expiry_price
                ) * put.open_interest

            payout[expiry_price] = total

        max_pain = min(
            payout,
            key=payout.get
        )

        return {

            "max_pain": max_pain,

            "payout": payout

        }