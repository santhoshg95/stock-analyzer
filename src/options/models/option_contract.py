"""
Option Contract Model
"""

from dataclasses import dataclass


@dataclass
class OptionContract:

    symbol: str

    expiry: str

    strike: float

    option_type: str

    last_price: float

    bid: float

    ask: float

    volume: int

    open_interest: int

    change_in_oi: int

    implied_volatility: float

    delta: float | None = None

    gamma: float | None = None

    theta: float | None = None

    vega: float | None = None