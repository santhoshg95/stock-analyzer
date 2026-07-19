"""
Liquidity Analysis

Analyzes tradability of option contracts.
"""

from src.options.models.option_chain import OptionChain


class LiquidityAnalysis:

    MIN_OPEN_INTEREST = 10000

    MIN_VOLUME = 1000

    MAX_SPREAD_PERCENT = 2.0

    def analyze(self, chain: OptionChain):

        contracts = chain.calls + chain.puts

        if not contracts:

            return {

                "status": "POOR",

                "confidence": 0,

                "average_spread": 0,

                "liquid_contracts": 0,

                "illiquid_contracts": 0,

                "reasons": [

                    "No option contracts available."

                ]

            }

        liquid = 0
        illiquid = 0

        spreads = []

        reasons = []

        for contract in contracts:

            if contract.ask <= 0:

                continue

            spread_percent = (
                (contract.ask - contract.bid)
                / contract.ask
            ) * 100

            spreads.append(spread_percent)

            is_liquid = (

                contract.open_interest >= self.MIN_OPEN_INTEREST

                and

                contract.volume >= self.MIN_VOLUME

                and

                spread_percent <= self.MAX_SPREAD_PERCENT

            )

            if is_liquid:

                liquid += 1

            else:

                illiquid += 1

        average_spread = (

            sum(spreads) / len(spreads)

            if spreads else 0

        )

        ratio = liquid / len(contracts)

        confidence = round(ratio * 100)

        if confidence >= 80:

            status = "EXCELLENT"

        elif confidence >= 60:

            status = "GOOD"

        elif confidence >= 40:

            status = "AVERAGE"

        else:

            status = "POOR"

        reasons.append(

            f"{liquid} out of {len(contracts)} contracts passed liquidity checks."

        )

        reasons.append(

            f"Average Bid/Ask Spread: {average_spread:.2f}%"

        )

        return {

            "status": status,

            "confidence": confidence,

            "average_spread": round(average_spread, 2),

            "liquid_contracts": liquid,

            "illiquid_contracts": illiquid,

            "reasons": reasons

        }