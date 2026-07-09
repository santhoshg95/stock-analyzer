"""
Decision Context Model

Every intelligence engine in the platform returns
this object.

Examples:
    - Market Engine
    - Sector Engine
    - Technical Engine
    - News Engine
    - Option Engine
    - Risk Engine
"""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class DecisionContext:

    # Engine Name
    engine: str

    # Current Status
    status: str

    # Raw Score
    score: float

    # Confidence Percentage
    confidence: float

    # Reasons supporting the decision
    reasons: List[str] = field(default_factory=list)

    # Warnings
    warnings: List[str] = field(default_factory=list)

    # Extra information
    metadata: Dict = field(default_factory=dict)

    def __str__(self):

        text = []

        text.append("=" * 80)
        text.append(f"ENGINE      : {self.engine}")
        text.append(f"STATUS      : {self.status}")
        text.append(f"SCORE       : {self.score}")
        text.append(f"CONFIDENCE  : {self.confidence}%")
        text.append("")

        if self.reasons:

            text.append("Reasons")

            for reason in self.reasons:
                text.append(f"  ✓ {reason}")

            text.append("")

        if self.warnings:

            text.append("Warnings")

            for warning in self.warnings:
                text.append(f"  ⚠ {warning}")

            text.append("")

        return "\n".join(text)