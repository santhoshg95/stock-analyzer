"""
Historical Downloader

Downloads historical OHLCV data.

Supports

- Yahoo Finance
- Future NSE provider
- Future Kite provider

Author:
    AI Research Platform
"""

from __future__ import annotations

import logging
import time
from abc import ABC
from abc import abstractmethod
from typing import Optional

import pandas as pd
import yfinance as yf

logger = logging.getLogger(__name__)


# ===========================================================
# Base Downloader
# ===========================================================


class HistoricalDownloader(ABC):
    """
    Abstract downloader.

    Every provider must return the same dataframe format.

    Columns

        Date
        Open
        High
        Low
        Close
        Adj Close
        Volume
    """

    @abstractmethod
    def download(
        self,
        symbol: str,
        period: str = "10y",
        interval: str = "1d",
    ) -> pd.DataFrame:
        raise NotImplementedError


# ===========================================================
# Yahoo Finance Downloader
# ===========================================================


class YahooDownloader(HistoricalDownloader):

    def __init__(
        self,
        retries: int = 3,
        retry_delay: int = 3,
    ) -> None:

        self.retries = retries
        self.retry_delay = retry_delay

    # -------------------------------------------------------

    def download(
        self,
        symbol: str,
        period: str = "10y",
        interval: str = "1d",
    ) -> pd.DataFrame:

        ticker = self._normalize_symbol(symbol)

        last_exception: Optional[Exception] = None

        for attempt in range(self.retries):

            try:

                logger.info(
                    "Downloading historical data for %s",
                    ticker,
                )

                df = yf.download(
                    ticker,
                    period=period,
                    interval=interval,
                    auto_adjust=False,
                    progress=False,
                    threads=False,
                )

                if df.empty:

                    raise ValueError(
                        f"No historical data found for {ticker}"
                    )

                df = self._normalize_dataframe(df)

                logger.info(
                    "Downloaded %d records for %s",
                    len(df),
                    ticker,
                )

                return df

            except Exception as ex:

                last_exception = ex

                logger.warning(
                    "Download failed (%d/%d): %s",
                    attempt + 1,
                    self.retries,
                    ex,
                )

                time.sleep(self.retry_delay)

        raise RuntimeError(
            f"Unable to download {ticker}"
        ) from last_exception

    # -------------------------------------------------------

    @staticmethod
    def _normalize_symbol(symbol: str) -> str:
        """
        Convert NSE symbols.

        INFY -> INFY.NS
        RELIANCE -> RELIANCE.NS
        """

        symbol = symbol.upper()

        if "." not in symbol:
            return f"{symbol}.NS"

        return symbol
    # -------------------------------------------------------

    @staticmethod
    def _normalize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
        """
        Normalize dataframe returned by providers.

        Standard Columns

        Date
        Open
        High
        Low
        Close
        Adj Close
        Volume
        """

        df = df.copy()

        # ---------------------------------------------
        # Reset index
        # ---------------------------------------------

        if "Date" not in df.columns:
            df.reset_index(inplace=True)

        # ---------------------------------------------
        # Flatten MultiIndex columns
        # ---------------------------------------------

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [col[0] for col in df.columns]

        # ---------------------------------------------
        # Standardize names
        # ---------------------------------------------

        rename_map = {
            "Adj Close": "Adj Close",
            "Adj_Close": "Adj Close",
            "Open": "Open",
            "High": "High",
            "Low": "Low",
            "Close": "Close",
            "Volume": "Volume",
            "Date": "Date",
        }

        df.rename(columns=rename_map, inplace=True)

        # ---------------------------------------------
        # Required columns
        # ---------------------------------------------

        required = [
            "Date",
            "Open",
            "High",
            "Low",
            "Close",
            "Volume",
        ]

        for column in required:

            if column not in df.columns:

                raise ValueError(
                    f"Missing required column '{column}'"
                )

        # ---------------------------------------------
        # Adj Close
        # ---------------------------------------------

        if "Adj Close" not in df.columns:
            df["Adj Close"] = df["Close"]

        # ---------------------------------------------
        # Date
        # ---------------------------------------------

        df["Date"] = pd.to_datetime(df["Date"])

        # ---------------------------------------------
        # Sort
        # ---------------------------------------------

        df.sort_values(
            by="Date",
            inplace=True,
        )

        # ---------------------------------------------
        # Remove duplicates
        # ---------------------------------------------

        df.drop_duplicates(
            subset="Date",
            keep="last",
            inplace=True,
        )

        # ---------------------------------------------
        # Numeric conversion
        # ---------------------------------------------

        numeric_columns = [
            "Open",
            "High",
            "Low",
            "Close",
            "Adj Close",
            "Volume",
        ]

        for column in numeric_columns:

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce",
            )

        # ---------------------------------------------
        # Missing values
        # ---------------------------------------------

        df.ffill(inplace=True)
        df.bfill(inplace=True)

        df.dropna(inplace=True)

        # ---------------------------------------------
        # Remove invalid candles
        # ---------------------------------------------

        df = df[
            (df["Open"] > 0)
            &
            (df["High"] > 0)
            &
            (df["Low"] > 0)
            &
            (df["Close"] > 0)
        ]

        # ---------------------------------------------
        # Volume
        # ---------------------------------------------

        df["Volume"] = (
            df["Volume"]
            .fillna(0)
            .astype("int64")
        )

        # ---------------------------------------------
        # Final order
        # ---------------------------------------------

        df = df[
            [
                "Date",
                "Open",
                "High",
                "Low",
                "Close",
                "Adj Close",
                "Volume",
            ]
        ]

        df.reset_index(
            drop=True,
            inplace=True,
        )

        return df


# ===========================================================
# Downloader Factory
# ===========================================================


class DownloaderFactory:

    """
    Factory responsible for returning
    the correct downloader.

    Future providers

        Yahoo

        NSE

        Kite

        AlphaVantage

        Polygon
    """

    _providers = {
        "yahoo": YahooDownloader,
    }

    @classmethod
    def create(
        cls,
        provider: str = "yahoo",
    ) -> HistoricalDownloader:

        provider = provider.lower()

        if provider not in cls._providers:

            raise ValueError(
                f"Unsupported provider : {provider}"
            )

        return cls._providers[provider]()


from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from dataclasses import dataclass
from typing import Dict, List


# ===========================================================
# Download Summary
# ===========================================================


@dataclass
class DownloadSummary:
    """
    Summary of batch historical downloads.
    """

    total_symbols: int
    success_count: int
    failed_count: int

    successful_symbols: List[str]
    failed_symbols: List[str]

    dataframes: Dict[str, pd.DataFrame]


# ===========================================================
# Batch Downloader
# ===========================================================


class BatchDownloader:
    """
    Downloads historical data for multiple symbols.

    Future Enhancements

        Async Download

        Rate Limiting

        Provider Failover

        Incremental Download

        Resume Support
    """

    def __init__(
        self,
        provider: str = "yahoo",
        workers: int = 5,
    ) -> None:

        self.downloader = DownloaderFactory.create(provider)
        self.workers = workers

    # -----------------------------------------------------

    def download_many(
        self,
        symbols: List[str],
        period: str = "10y",
        interval: str = "1d",
    ) -> DownloadSummary:

        successful = []
        failed = []

        data = {}

        logger.info(
            "Downloading historical data for %d symbols",
            len(symbols),
        )

        with ThreadPoolExecutor(
            max_workers=self.workers
        ) as executor:

            futures = {
                executor.submit(
                    self.downloader.download,
                    symbol,
                    period,
                    interval,
                ): symbol
                for symbol in symbols
            }

            for future in as_completed(futures):

                symbol = futures[future]

                try:

                    df = future.result()

                    data[symbol] = df

                    successful.append(symbol)

                    logger.info(
                        "[SUCCESS] %s (%d records)",
                        symbol,
                        len(df),
                    )

                except Exception as ex:

                    failed.append(symbol)

                    logger.exception(
                        "[FAILED] %s : %s",
                        symbol,
                        ex,
                    )

        logger.info(
            "Download Complete : %d success / %d failed",
            len(successful),
            len(failed),
        )

        return DownloadSummary(
            total_symbols=len(symbols),
            success_count=len(successful),
            failed_count=len(failed),
            successful_symbols=successful,
            failed_symbols=failed,
            dataframes=data,
        )

    # -----------------------------------------------------

    def retry_failed(
        self,
        summary: DownloadSummary,
        period: str = "10y",
        interval: str = "1d",
    ) -> DownloadSummary:
        """
        Retry only failed downloads.
        """

        if not summary.failed_symbols:
            return summary

        logger.info(
            "Retrying %d failed symbols",
            len(summary.failed_symbols),
        )

        retry = self.download_many(
            summary.failed_symbols,
            period,
            interval,
        )

        summary.successful_symbols.extend(
            retry.successful_symbols
        )

        summary.failed_symbols = retry.failed_symbols

        summary.success_count += retry.success_count

        summary.failed_count = len(retry.failed_symbols)

        summary.dataframes.update(
            retry.dataframes
        )

        return summary