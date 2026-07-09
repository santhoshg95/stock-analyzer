"""
AI Score Result
"""

from dataclasses import dataclass, field
from typing import List

from src.factors.factor_result import FactorResult


@dataclass
class AIScoreResult:

    total_score: float

    max_score: float

    percentage: float

    factors: List[FactorResult] = field(default_factory=list)

    recommendation: str = "WAIT"

    confidence: float = 0