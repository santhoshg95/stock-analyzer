"""
Greeks Analysis Result
"""

from dataclasses import dataclass, field


@dataclass(slots=True)
class GreeksAnalysisResult:
    """
    Aggregate Greeks calculated from the option chain.
    """

    average_delta: float

    average_gamma: float

    average_theta: float

    average_vega: float

    average_rho: float

    confidence: int

    market_bias: str

    reasons: list[str] = field(default_factory=list)