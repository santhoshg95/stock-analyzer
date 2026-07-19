"""
Max Pain Analysis Result
"""

from dataclasses import dataclass, field


@dataclass(slots=True)
class MaxPainResult:
    """
    Result of Max Pain calculation.
    """

    max_pain: float | None

    payout: dict[float, float] = field(default_factory=dict)