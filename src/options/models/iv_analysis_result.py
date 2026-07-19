"""
IV Analysis Result
"""

from dataclasses import dataclass, field


@dataclass(slots=True)
class IVAnalysisResult:

    average_iv: float

    status: str

    confidence: int

    reasons: list[str] = field(default_factory=list)