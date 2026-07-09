"""
AI Score Model
"""

from dataclasses import dataclass


@dataclass
class AIScore:

    market: float = 0

    sector: float = 0

    technical: float = 0

    candlestick: float = 0

    breakout: float = 0

    relative_strength: float = 0

    news: float = 0

    option: float = 0

    total: float = 0

    max_available: float = 0

    percentage: float = 0