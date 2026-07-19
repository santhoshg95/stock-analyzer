"""
Market Regime
"""

from dataclasses import dataclass, field


@dataclass(slots=True)
class MarketRegime:

    regime: str

    confidence: float

    reasons: list[str] = field(default_factory=list)