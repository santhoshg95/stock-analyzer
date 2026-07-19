"""
Historical Data Cache

Author : AI Research Platform
Purpose:
    Local parquet cache for historical OHLCV data.

Responsibilities:
    - Read cache
    - Write cache
    - Delete cache
    - Cache expiry
"""

from __future__ import annotations

from pathlib import Path
from datetime import datetime, timedelta

import pandas as pd


class HistoricalCache:
    """
    Disk cache for historical data.

    Structure

    .cache/
        historical/
            RELIANCE.parquet
            INFY.parquet
            TCS.parquet
    """

    def __init__(
        self,
        cache_directory: str = ".cache/historical",
        expiry_days: int = 1,
    ) -> None:

        self.cache_dir = Path(cache_directory)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        self.expiry_days = expiry_days

    def _path(self, symbol: str) -> Path:
        return self.cache_dir / f"{symbol.upper()}.parquet"

    def exists(self, symbol: str) -> bool:
        return self._path(symbol).exists()

    def is_expired(self, symbol: str) -> bool:

        path = self._path(symbol)

        if not path.exists():
            return True

        modified = datetime.fromtimestamp(path.stat().st_mtime)

        return datetime.now() - modified > timedelta(days=self.expiry_days)

    def read(self, symbol: str) -> pd.DataFrame:

        path = self._path(symbol)

        if not path.exists():
            return pd.DataFrame()

        try:
            return pd.read_parquet(path)

        except Exception:
            return pd.DataFrame()

    def write(
        self,
        symbol: str,
        dataframe: pd.DataFrame,
    ) -> None:

        if dataframe.empty:
            return

        dataframe.to_parquet(
            self._path(symbol),
            index=False,
        )

    def delete(self, symbol: str) -> None:

        path = self._path(symbol)

        if path.exists():
            path.unlink()

    def clear(self) -> None:

        for file in self.cache_dir.glob("*.parquet"):
            file.unlink()