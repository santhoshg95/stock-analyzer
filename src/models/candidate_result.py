"""
Candidate Result Model
"""

from dataclasses import dataclass


@dataclass
class CandidateResult:

    symbol: str

    score: float

    percentage: float

    market: str

    technical: str