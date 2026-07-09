"""
Factor Result

Standard output returned by every factor.
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class FactorResult:

    name: str

    score: float

    weight: float

    confidence: float

    contribution: float

    reasons: List[str] = field(default_factory=list)

    metadata: dict = field(default_factory=dict)