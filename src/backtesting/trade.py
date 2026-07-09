"""
Trade Model
"""

from dataclasses import dataclass


@dataclass
class Trade:

    entry_price: float

    exit_price: float

    quantity: int

    pnl: float

    result: str