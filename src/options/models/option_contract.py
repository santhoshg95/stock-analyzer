"""
Option Contract Model
"""

from dataclasses import dataclass


@dataclass(slots=True)
class OptionContract:
    """
    Represents a single option contract.
    """

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

    # Greeks

    delta: float | None = None

    gamma: float | None = None

    theta: float | None = None

    vega: float | None = None

    rho: float | None = None

    # Exchange quote's percentage/net change when supplied by the broker.
    price_change: float | None = None

    # Exchange lot size, supplied by the live instrument master when available.
    lot_size: int = 1

    greeks_source: str | None = None

    change_in_oi_reliable: bool = False

    quote_timestamp: str | None = None

    quote_is_stale: bool = False
