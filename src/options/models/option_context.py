"""
Option Context

Stores all option-related intelligence for a stock.
"""

from dataclasses import dataclass

from src.options.models.option_analysis import OptionAnalysis
from src.options.models.option_chain import OptionChain


@dataclass(slots=True)
class OptionContext:
    """
    Shared option context used throughout the AI pipeline.

    Contains:
        - Raw Option Chain
        - Final Option Analysis
    """

    chain: OptionChain | None = None

    analysis: OptionAnalysis | None = None