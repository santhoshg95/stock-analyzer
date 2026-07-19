"""
Dealer Position Analysis Result
"""

from dataclasses import dataclass, field


@dataclass(slots=True)
class DealerPositionResult:
    """
    Dealer positioning inferred from option chain.
    """

    market_bias: str

    support_strike: float | None

    resistance_strike: float | None

    confidence: float

    score: float

    reasons: list[str] = field(default_factory=list)