"""
Factor Score Model
"""

from dataclasses import dataclass


@dataclass(slots=True)
class FactorScore:
    """
    Represents the score of one intelligence factor.
    """

    name: str

    score: float

    confidence: float

    weight: float

    reason: str