"""
Trade Plan Model
"""

from dataclasses import dataclass


@dataclass
class TradePlan:

    entry: float

    stop_loss: float

    target1: float

    target2: float

    risk: float

    reward: float

    risk_reward: float

    quality: str