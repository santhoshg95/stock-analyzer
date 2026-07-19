"""
IV Percentile Result
"""

from dataclasses import dataclass, field


@dataclass(slots=True)
class IVPercentileResult:

    percentile: float

    status: str

    confidence: float

    score: float

    reasons: list[str] = field(default_factory=list)