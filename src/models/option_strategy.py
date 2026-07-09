"""
Option Strategy Model
"""

from dataclasses import dataclass


@dataclass
class OptionStrategy:

    name: str

    market_bias: str

    volatility: str

    description: str