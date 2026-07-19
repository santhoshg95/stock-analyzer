"""
Volatility Analysis Result
"""

from dataclasses import dataclass, field


@dataclass(slots=True)
class VolatilityAnalysisResult:
    """
    ATR based volatility analysis.
    """

    volatility: str

    confidence: float

    score: float

    atr: float

    atr_percentage: float

    expected_move: float

    reasons: list[str] = field(default_factory=list)