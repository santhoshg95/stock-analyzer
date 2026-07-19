"""
Option Intelligence Engine

Combines all option analyses into a single OptionAnalysis.
"""

from src.options.analysis.iv_analysis import IVAnalysis
from src.options.analysis.liquidity_analysis import LiquidityAnalysis
from src.options.analysis.max_pain import MaxPainAnalysis
from src.options.analysis.oi_analysis import OIAnalysis
from src.options.analysis.pcr_analysis import PCRAnalysis
from src.options.models.option_analysis import OptionAnalysis
from src.options.models.option_chain import OptionChain


class OptionEngine:

    def __init__(self):

        self.oi = OIAnalysis()

        self.pcr = PCRAnalysis()

        self.max_pain = MaxPainAnalysis()

        self.liquidity = LiquidityAnalysis()

        self.iv = IVAnalysis()

    def analyze(self, chain: OptionChain) -> OptionAnalysis:

        oi = self.oi.analyze(chain)

        pcr = self.pcr.analyze(chain)

        max_pain = self.max_pain.analyze(chain)

        liquidity = self.liquidity.analyze(chain)

        iv = self.iv.analyze(chain)

        confidence = 50

        reasons = []

        # PCR

        if pcr["sentiment"] == "BULLISH":

            confidence += 20

            reasons.append(

                "PCR indicates bullish positioning."

            )

        elif pcr["sentiment"] == "BEARISH":

            confidence -= 20

            reasons.append(

                "PCR indicates bearish positioning."

            )

        # Liquidity

        confidence += int(

            liquidity["confidence"] / 10

        )

        reasons.extend(

            liquidity["reasons"]

        )

        # IV

        confidence += int(

            iv["confidence"] / 20

        )

        reasons.extend(

            iv["reasons"]

        )

        # Max Pain

        if max_pain["max_pain"] is not None:

            reasons.append(

                f"Maximum Pain strike is {max_pain['max_pain']}."

            )

        confidence = max(

            0,

            min(

                confidence,

                100

            )

        )

        return OptionAnalysis(

            status=pcr["sentiment"],

            confidence=confidence,

            score=confidence,

            pcr=pcr["pcr"],

            max_pain=max_pain["max_pain"],

            iv_rank=iv["average_iv"],

            strongest_support=oi["put_support"],

            strongest_resistance=oi["call_resistance"],

            suggested_strategy=None,

            reasons=reasons

        )