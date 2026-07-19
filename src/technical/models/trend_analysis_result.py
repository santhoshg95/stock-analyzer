"""
Trend Analysis Result
"""

from dataclasses import dataclass, field


@dataclass(slots=True)
class TrendAnalysisResult:
    """
    Result of trend analysis.
    """

    trend: str

    confidence: float

    score: float

    ema20: float

    ema50: float

    ema200: float

    reasons: list[str] = field(default_factory=list)