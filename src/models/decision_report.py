"""
Decision Report
"""

from dataclasses import dataclass
from typing import List

from src.models.strategy import Strategy


@dataclass
class DecisionReport:

    allowed: List[Strategy]

    blocked: List[Strategy]

    reason: str