"""
Trade Plan Model
"""

from dataclasses import dataclass, field


@dataclass(slots=True)
class TradePlan:
    """
    Complete executable trade plan.
    """

    symbol: str

    strategy: str

    action: str

    entry_price: float

    stop_loss: float

    target_1: float

    target_2: float

    target_3: float

    quantity: int

    capital_required: float

    risk_reward_ratio: float

    maximum_loss: float

    expected_profit: float

    trailing_stop: bool

    holding_period: str

    reasons: list[str] = field(default_factory=list)