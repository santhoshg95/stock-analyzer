"""Historical OHLCV data adapter backed by Zerodha Kite Connect."""

from __future__ import annotations

from pathlib import Path
from threading import RLock

import pandas as pd

from src.providers.kite_provider import KiteProvider


class KiteDataProvider:
    """Matches the ``DataProvider.get_data`` interface using live Kite data."""

    def __init__(
        self,
        provider: KiteProvider | None = None,
        long_history_cache_directory: str | Path = ".cache/kite_long_history",
    ):
        self.provider = provider or KiteProvider()
        self._history_cache = {}
        self._long_history_cache = {}
        self._long_history_cache_directory = Path(long_history_cache_directory)
        self._long_history_cache_lock = RLock()

    def _long_history_path(self, symbol: str, period: str) -> Path:
        safe_period = period.lower().replace("/", "_").replace("\\", "_")
        return self._long_history_cache_directory / f"{symbol}_{safe_period}.parquet"

    def get_data(self, symbol: str):
        key = symbol.upper().removesuffix(".NS")
        if key not in self._history_cache:
            self._history_cache[key] = self.provider.get_historical_data(key)
        return self._history_cache[key].copy()

    def get_long_history(self, symbol: str, period: str = "10y"):
        key = (symbol.upper().removesuffix(".NS"), period)
        with self._long_history_cache_lock:
            if key in self._long_history_cache:
                return self._long_history_cache[key].copy()

            cache_path = self._long_history_path(*key)
            if cache_path.exists():
                try:
                    cached = pd.read_parquet(cache_path)
                    if not cached.empty:
                        self._long_history_cache[key] = cached
                        return cached.copy()
                except (OSError, ValueError):
                    # A partial or incompatible cache file is treated as a miss.
                    pass

            history = self.provider.get_historical_data(key[0], period=period)
            self._long_history_cache[key] = history
            if history is not None and not history.empty:
                cache_path.parent.mkdir(parents=True, exist_ok=True)
                history.to_parquet(cache_path)
            return self._long_history_cache[key].copy()

    def get_symbols(self) -> list[str]:
        """Get the current F&O equity universe directly from Kite."""
        instruments = self.provider.kite.instruments("NFO")
        return sorted(
            {
                str(item["name"]).strip().upper()
                for item in instruments
                if item.get("instrument_type") == "FUT" and item.get("name")
            }
        )
