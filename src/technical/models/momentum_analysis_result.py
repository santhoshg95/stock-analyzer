"""
Momentum Analysis Result
"""

from dataclasses import dataclass, field


@dataclass(slots=True)
class MomentumAnalysisResult:
    """
    RSI + ADX analysis.
    """

    momentum: str

    confidence: float

    score: float

    rsi: float

    adx: float

    reasons: list[str] = field(default_factory=list)