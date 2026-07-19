"""
Put Call Ratio Analysis
"""

from src.options.models.option_chain import OptionChain


class PCRAnalysis:

    def analyze(self, chain: OptionChain):

        call_oi = sum(c.open_interest for c in chain.calls)

        put_oi = sum(p.open_interest for p in chain.puts)

        if call_oi == 0:

            return {

                "pcr": 0,

                "sentiment": "UNKNOWN"

            }

        pcr = put_oi / call_oi

        if pcr > 1.2:

            sentiment = "BULLISH"

        elif pcr < 0.8:

            sentiment = "BEARISH"

        else:

            sentiment = "NEUTRAL"

        return {

            "pcr": round(pcr, 2),

            "sentiment": sentiment

        }