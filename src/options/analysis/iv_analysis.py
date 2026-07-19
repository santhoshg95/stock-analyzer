"""
Implied Volatility Analysis
"""

from src.options.models.option_chain import OptionChain


class IVAnalysis:

    LOW_IV = 15

    HIGH_IV = 25

    VERY_HIGH_IV = 35

    def analyze(self, chain: OptionChain):

        contracts = chain.calls + chain.puts

        if not contracts:

            return {

                "average_iv": 0,

                "status": "UNKNOWN",

                "confidence": 0,

                "reasons": [

                    "No option contracts available."

                ]

            }

        ivs = [

            c.implied_volatility

            for c in contracts

            if c.implied_volatility > 0

        ]

        if not ivs:

            return {

                "average_iv": 0,

                "status": "UNKNOWN",

                "confidence": 0,

                "reasons": [

                    "No IV values available."

                ]

            }

        average_iv = sum(ivs) / len(ivs)

        reasons = []

        if average_iv < self.LOW_IV:

            status = "LOW"

            confidence = 20

            reasons.append(

                "Premiums are cheap."

            )

            reasons.append(

                "Not attractive for option selling."

            )

        elif average_iv < self.HIGH_IV:

            status = "NORMAL"

            confidence = 60

            reasons.append(

                "Premiums are fairly priced."

            )

        elif average_iv < self.VERY_HIGH_IV:

            status = "HIGH"

            confidence = 85

            reasons.append(

                "Premiums are attractive for option selling."

            )

        else:

            status = "VERY_HIGH"

            confidence = 95

            reasons.append(

                "Premiums are very expensive."

            )

            reasons.append(

                "High premium collection opportunity."

            )

        return {

            "average_iv": round(

                average_iv,

                2

            ),

            "status": status,

            "confidence": confidence,

            "reasons": reasons

        }