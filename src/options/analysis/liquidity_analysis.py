"""
Liquidity Analysis
"""

from src.options.models.liquidity_analysis_result import LiquidityAnalysisResult
from src.options.models.option_chain import OptionChain


class LiquidityAnalysis:

    MIN_OPEN_INTEREST = 10000

    MIN_VOLUME = 1000

    MAX_SPREAD_PERCENT = 2.0

    def analyze(self, chain: OptionChain) -> LiquidityAnalysisResult:

        contracts = chain.calls + chain.puts

        if not contracts:

            return LiquidityAnalysisResult(

                status="POOR",

                confidence=0,

                average_spread=0,

                liquid_contracts=0,

                illiquid_contracts=0,

                reasons=[

                    "No option contracts available."

                ]

            )

        liquid = 0
        illiquid = 0

        spreads = []

        reasons = []

        for contract in contracts:

            if contract.ask <= 0:

                continue

            spread = (

                (contract.ask - contract.bid)

                / contract.ask

            ) * 100

            spreads.append(spread)

            if (

                contract.open_interest >= self.MIN_OPEN_INTEREST

                and

                contract.volume >= self.MIN_VOLUME

                and

                spread <= self.MAX_SPREAD_PERCENT

            ):

                liquid += 1

            else:

                illiquid += 1

        average = (

            sum(spreads)

            / len(spreads)

            if spreads

            else 0

        )

        confidence = round(

            (liquid / len(contracts))

            * 100

        )

        if confidence >= 80:

            status = "EXCELLENT"

        elif confidence >= 60:

            status = "GOOD"

        elif confidence >= 40:

            status = "AVERAGE"

        else:

            status = "POOR"

        reasons.append(

            f"{liquid} of {len(contracts)} contracts are liquid."

        )

        reasons.append(

            f"Average spread {average:.2f}%"

        )

        return LiquidityAnalysisResult(

            status=status,

            confidence=confidence,

            average_spread=round(

                average,

                2

            ),

            liquid_contracts=liquid,

            illiquid_contracts=illiquid,

            reasons=reasons

        )