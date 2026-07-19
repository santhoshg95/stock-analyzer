"""Historical OHLCV data adapter backed by Zerodha Kite Connect."""

from __future__ import annotations

from src.providers.kite_provider import KiteProvider


class KiteDataProvider:
    """Matches the ``DataProvider.get_data`` interface using live Kite data."""

    def __init__(self, provider: KiteProvider | None = None):
        self.provider = provider or KiteProvider()

    def get_data(self, symbol: str):
        return self.provider.get_historical_data(symbol)

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
