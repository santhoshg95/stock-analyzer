"""
Historical Intelligence Engine

Combines historical data repository and statistics engine to build
a comprehensive intelligence profile for a stock.

Author:
    AI Research Platform
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional

import pandas as pd

from .repository import HistoricalRepository
from .statistics.statistics_engine import HistoricalStatisticsEngine


@dataclass
class HistoricalIntelligence:

    symbol: str

    start_date: str
    end_date: str

    records: int

    statistics: Dict[str, Any]

    metadata: Dict[str, Any]


class HistoricalIntelligenceEngine:

    def __init__(
        self,
        repository: Optional[HistoricalRepository] = None,
    ) -> None:

        self.repository = repository or HistoricalRepository()

        self.statistics_engine = HistoricalStatisticsEngine()

    # -------------------------------------------------------------

    def analyze(
        self,
        symbol: str,
        period: str = "10y",
    ) -> HistoricalIntelligence:

        dataframe = self.repository.get_history(
            symbol=symbol,
            period=period,
        )

        return self.from_dataframe(
            symbol=symbol,
            dataframe=dataframe,
        )

    # -------------------------------------------------------------

    def from_dataframe(
        self,
        symbol: str,
        dataframe: pd.DataFrame,
    ) -> HistoricalIntelligence:

        if dataframe.empty:

            raise ValueError(
                f"No historical data available for {symbol}"
            )

        statistics = self.statistics_engine.calculate(
            dataframe
        )

        metadata = self._metadata(
            dataframe
        )

        return HistoricalIntelligence(

            symbol=symbol.upper(),

            start_date=str(
                dataframe["Date"].min().date()
            ),

            end_date=str(
                dataframe["Date"].max().date()
            ),

            records=len(dataframe),

            statistics=statistics,

            metadata=metadata,
        )

    # -------------------------------------------------------------

    def as_dict(
        self,
        symbol: str,
        period: str = "10y",
    ) -> Dict[str, Any]:

        profile = self.analyze(
            symbol=symbol,
            period=period,
        )

        return asdict(profile)

    # -------------------------------------------------------------

    @staticmethod
    def _metadata(
        dataframe: pd.DataFrame,
    ) -> Dict[str, Any]:

        return {

            "first_close": float(
                dataframe["Close"].iloc[0]
            ),

            "last_close": float(
                dataframe["Close"].iloc[-1]
            ),

            "highest_close": float(
                dataframe["Close"].max()
            ),

            "lowest_close": float(
                dataframe["Close"].min()
            ),

            "highest_volume": float(
                dataframe["Volume"].max()
            ),

            "lowest_volume": float(
                dataframe["Volume"].min()
            ),

            "average_close": float(
                dataframe["Close"].mean()
            ),

            "average_volume": float(
                dataframe["Volume"].mean()
            ),
        }

    # -------------------------------------------------------------

    def summary(
        self,
        symbol: str,
        period: str = "10y",
    ) -> Dict[str, Any]:

        profile = self.analyze(
            symbol=symbol,
            period=period,
        )

        return {

            "symbol": profile.symbol,

            "records": profile.records,

            "start_date": profile.start_date,

            "end_date": profile.end_date,

            "overall_score": profile.statistics.get(
                "overall_score",
                0.0,
            ),

            "quality": profile.statistics.get(
                "quality",
                "UNKNOWN",
            ),

            "cagr": profile.statistics.get(
                "cagr",
                0.0,
            ),

            "annual_return": profile.statistics.get(
                "annual_return",
                0.0,
            ),

            "volatility": profile.statistics.get(
                "volatility",
                0.0,
            ),

            "max_drawdown": profile.statistics.get(
                "max_drawdown",
                0.0,
            ),

            "sharpe_ratio": profile.statistics.get(
                "sharpe_ratio",
                0.0,
            ),

            "win_rate": profile.statistics.get(
                "win_rate",
                0.0,
            ),

            "liquidity_score": profile.statistics.get(
                "liquidity_score",
                0.0,
            ),
        }

    # -------------------------------------------------------------

    def health_check(
        self,
        symbol: str = "AAPL",
    ) -> bool:

        try:

            self.analyze(symbol)

            return True

        except Exception:

            return False