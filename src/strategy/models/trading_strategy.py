"""
Trading Strategy Model
"""

from dataclasses import dataclass, field


@dataclass(slots=True)
class TradingStrategy:
    """
    Strategy selected by the AI.
    """

    name: str

    asset_type: str

    direction: str

    confidence: float

    expected_holding_period: str

    reasons: list[str] = field(default_factory=list)