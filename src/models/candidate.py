"""
Candidate Model
"""

from dataclasses import dataclass


@dataclass
class Candidate:

    symbol: str

    sector: str

    score: float

    technical_score: float

    market_score: float

    sector_score: float

    volume_score: float

    breakout_score: float

    relative_strength: float

    trade_direction: str

    confidence: float