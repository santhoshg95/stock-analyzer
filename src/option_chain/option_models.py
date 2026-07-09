"""
Option Chain Models
"""

from dataclasses import dataclass


@dataclass
class OptionStrike:

    strike: float

    option_type: str

    ltp: float

    bid: float

    ask: float

    volume: int

    open_interest: int

    iv: float | None = None

    delta: float | None = None

    gamma: float | None = None

    theta: float | None = None

    vega: float | None = None


@dataclass
class OptionChain:

    symbol: str

    expiry: str

    spot_price: float

    calls: list[OptionStrike]

    puts: list[OptionStrike]