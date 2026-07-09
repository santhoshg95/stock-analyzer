"""
Strategy Report
"""

from dataclasses import dataclass
from typing import List

from src.models.option_strategy import OptionStrategy


@dataclass
class StrategyReport:

    symbol: str

    recommended: List[OptionStrategy]

    rejected: List[OptionStrategy]

    reason: str