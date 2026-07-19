"""
Candlestick Pattern
"""

from dataclasses import dataclass


@dataclass(slots=True)
class CandlestickPattern:
    """
    Represents one detected candlestick pattern.
    """

    name: str

    bullish: bool

    strength: float

    confidence: float

    reason: str