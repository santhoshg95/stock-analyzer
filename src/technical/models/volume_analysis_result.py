"""
Volume Analysis Result
"""

from dataclasses import dataclass, field


@dataclass(slots=True)
class VolumeAnalysisResult:
    """
    Volume analysis result.
    """

    status: str

    confidence: float

    score: float

    current_volume: float

    average_volume: float

    relative_volume: float

    reasons: list[str] = field(default_factory=list)