"""
Liquidity Analysis Result
"""

from dataclasses import dataclass, field


@dataclass(slots=True)
class LiquidityAnalysisResult:

    status: str

    confidence: int

    average_spread: float

    liquid_contracts: int

    illiquid_contracts: int

    reasons: list[str] = field(default_factory=list)