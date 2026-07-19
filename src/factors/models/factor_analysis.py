"""
Factor Analysis

Aggregated factor results.
"""

from dataclasses import dataclass, field

from src.factors.models.factor_score import FactorScore


@dataclass(slots=True)
class FactorAnalysis:
    """
    Final factor analysis.
    """

    overall_score: float = 0.0

    confidence: float = 0.0

    factors: list[FactorScore] = field(default_factory=list)

    bullish_factors: int = 0

    bearish_factors: int = 0

    neutral_factors: int = 0