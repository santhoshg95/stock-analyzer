"""
Gamma Exposure Result
"""

from dataclasses import dataclass, field


@dataclass(slots=True)
class GammaExposureResult:
    """
    Gamma exposure analysis result.
    """

    net_gamma: float

    gamma_flip: float | None

    status: str

    confidence: float

    score: float

    reasons: list[str] = field(default_factory=list)