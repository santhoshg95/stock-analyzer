"""
Base Signal Model

Every trading signal in the system follows this structure.

Examples:
- Trend Signal
- Momentum Signal
- Volume Signal
- Support Signal
- Option Chain Signal
- News Signal
"""

from dataclasses import dataclass, asdict


@dataclass
class Signal:
    """
    Generic Trading Signal
    """

    # --------------------------------------------------
    # Identity
    # --------------------------------------------------

    name: str

    # --------------------------------------------------
    # Interpretation
    # --------------------------------------------------

    direction: str

    # Examples:
    # Bullish
    # Bearish
    # Neutral

    # --------------------------------------------------
    # Strength
    # --------------------------------------------------

    strength: float

    # 0 - 100

    # --------------------------------------------------
    # Confidence
    # --------------------------------------------------

    confidence: float

    # 0 - 100

    # --------------------------------------------------
    # Explanation
    # --------------------------------------------------

    reason: str

    # --------------------------------------------------
    # Utility Methods
    # --------------------------------------------------

    def to_dict(self):

        return asdict(self)

    def __str__(self):

        return (
            f"{self.name} | "
            f"{self.direction} | "
            f"Strength={self.strength:.1f} | "
            f"Confidence={self.confidence:.1f}"
        )

    def __repr__(self):

        return self.__str__()