"""
Option Intelligence Engine

Orchestrates all option analyses and builds the final OptionAnalysis.
"""

from src.options.analysis.greeks_analysis import GreeksAnalysis
from src.options.analysis.iv_analysis import IVAnalysis
from src.options.analysis.liquidity_analysis import LiquidityAnalysis
from src.options.analysis.max_pain import MaxPainAnalysis
from src.options.analysis.oi_analysis import OIAnalysis
from src.options.analysis.pcr_analysis import PCRAnalysis

from src.options.models.option_analysis import OptionAnalysis
from src.options.models.option_chain import OptionChain

from src.options.services.analysis_builder import OptionAnalysisBuilder
from src.options.services.confidence_calculator import (
    OptionConfidenceCalculator,
)
from src.options.services.strategy_selector import (
    OptionStrategySelector,
)


class OptionEngine:
    """
    Central orchestrator for option intelligence.

    Responsibilities:
        - Execute analysis modules
        - Calculate confidence
        - Select strategy
        - Build OptionAnalysis
    """

    def __init__(self):

        self.oi = OIAnalysis()

        self.pcr = PCRAnalysis()

        self.max_pain = MaxPainAnalysis()

        self.liquidity = LiquidityAnalysis()

        self.iv = IVAnalysis()

        self.greeks = GreeksAnalysis()

        self.confidence = OptionConfidenceCalculator()

        self.strategy = OptionStrategySelector()

        self.builder = OptionAnalysisBuilder()

    def analyze(
        self,
        chain: OptionChain,
    ) -> OptionAnalysis:

        # ----------------------------------------------------
        # Execute Analyses
        # ----------------------------------------------------

        oi = self.oi.analyze(chain)

        pcr = self.pcr.analyze(chain)

        liquidity = self.liquidity.analyze(chain)

        iv = self.iv.analyze(chain)

        max_pain = self.max_pain.analyze(chain)

        greeks = self.greeks.analyze(chain)

        # ----------------------------------------------------
        # Calculate Confidence
        # ----------------------------------------------------

        confidence, reasons = self.confidence.calculate(

            pcr=pcr,

            liquidity=liquidity,

            iv=iv,

            greeks=greeks,

        )

        # ----------------------------------------------------
        # Strategy Recommendation
        # ----------------------------------------------------

        strategy = self.strategy.select(

            pcr=pcr,

            iv=iv,

            greeks=greeks,

        )

        # ----------------------------------------------------
        # Max Pain Reason
        # ----------------------------------------------------

        if max_pain.max_pain is not None:

            reasons.append(

                f"Maximum Pain strike is {max_pain.max_pain}."

            )

        # ----------------------------------------------------
        # Build Final Analysis
        # ----------------------------------------------------

        return self.builder.build(

            confidence=confidence,

            reasons=reasons,

            strategy=strategy,

            oi=oi,

            pcr=pcr,

            iv=iv,

            max_pain=max_pain,

        )