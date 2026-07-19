"""
Option Context

Stores all option-related intelligence for a stock.
"""

from dataclasses import dataclass, field

from src.options.models.option_analysis import OptionAnalysis
from src.options.models.option_chain import OptionChain


@dataclass
class OptionContext:

    chain: OptionChain | None = None

    analysis: OptionAnalysis | None = None

    pcr: float | None = None

    max_pain: float | None = None

    iv_rank: float | None = None

    strongest_support: float | None = None

    strongest_resistance: float | None = None

    suggested_strategy: str | None = None

    confidence: float = 0.0

    reasons: list[str] = field(default_factory=list)