"""
Position Size Model
"""

from dataclasses import dataclass


@dataclass
class PositionSize:

    quantity: int

    quantity_risk: int

    quantity_capital: int

    capital_used: float

    risk_amount: float

    actual_risk: float

    risk_per_share: float