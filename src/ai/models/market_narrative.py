"""
Market Narrative
"""

from dataclasses import dataclass, field


@dataclass(slots=True)
class MarketNarrative:
    """
    Human-readable explanation of the current market state.
    """

    summary: str

    expected_behavior: str

    confidence: float

    key_points: list[str] = field(default_factory=list)