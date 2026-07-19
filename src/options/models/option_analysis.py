"""
Option Analysis Result
"""

from dataclasses import dataclass, field


@dataclass
class OptionAnalysis:

    status: str

    confidence: float

    score: float

    pcr: float | None = None

    max_pain: float | None = None

    iv_rank: float | None = None

    strongest_support: float | None = None

    strongest_resistance: float | None = None

    suggested_strategy: str | None = None

    reasons: list[str] = field(default_factory=list)