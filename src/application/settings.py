"""Runtime settings for the public application layer."""

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class PlatformSettings:
    """Safe defaults that can be overridden through environment variables."""

    capital: float = 100_000.0
    risk_percent: float = 1.0
    allow_live_trading: bool = False
    market_data_source: str = "kite"

    @classmethod
    def from_environment(cls) -> "PlatformSettings":
        capital = float(os.getenv("TRADING_CAPITAL", "100000"))
        risk_percent = float(os.getenv("TRADING_RISK_PERCENT", "1"))
        allow_live = os.getenv("ALLOW_LIVE_TRADING", "false").lower() == "true"
        market_data_source = os.getenv("MARKET_DATA_SOURCE", "kite").lower()
        if capital <= 0:
            raise ValueError("TRADING_CAPITAL must be positive")
        if not 0 < risk_percent <= 100:
            raise ValueError("TRADING_RISK_PERCENT must be between 0 and 100")
        if market_data_source not in {"kite", "cache"}:
            raise ValueError("MARKET_DATA_SOURCE must be 'kite' or 'cache'")
        return cls(
            capital=capital,
            risk_percent=risk_percent,
            allow_live_trading=allow_live,
            market_data_source=market_data_source,
        )
