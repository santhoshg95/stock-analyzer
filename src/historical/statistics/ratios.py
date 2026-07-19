"""
Ratio Calculator

Calculates risk-adjusted performance ratios.

Author:
    AI Research Platform
"""

from __future__ import annotations

import numpy as np
import pandas as pd


class RatioCalculator:

    TRADING_DAYS = 252

    def __init__(
        self,
        risk_free_rate: float = 0.06,
    ) -> None:

        self.risk_free_rate = risk_free_rate

    # -----------------------------------------------------

    def calculate(
        self,
        df: pd.DataFrame,
    ) -> dict:

        returns = (
            df["Close"]
            .pct_change()
            .dropna()
        )

        volatility = (
            returns.std()
            * np.sqrt(self.TRADING_DAYS)
        )

        downside = (
            returns[returns < 0]
            .std()
            * np.sqrt(self.TRADING_DAYS)
        )

        cumulative = (
            1 + returns
        ).cumprod()

        peak = cumulative.cummax()

        drawdown = (
            cumulative - peak
        ) / peak

        max_drawdown = abs(
            drawdown.min()
        )

        annual_return = (
            returns.mean()
            * self.TRADING_DAYS
        )

        sharpe = self.sharpe_ratio(
            annual_return,
            volatility,
        )

        sortino = self.sortino_ratio(
            annual_return,
            downside,
        )

        calmar = self.calmar_ratio(
            annual_return,
            max_drawdown,
        )

        return {

            "sharpe_ratio": sharpe,

            "sortino_ratio": sortino,

            "calmar_ratio": calmar,

            "ratio_score": self.score(
                sharpe,
                sortino,
                calmar,
            ),
        }

    # -----------------------------------------------------

    def sharpe_ratio(
        self,
        annual_return: float,
        volatility: float,
    ) -> float:

        if volatility <= 0:
            return 0.0

        return float(

            (
                annual_return
                - self.risk_free_rate
            )

            / volatility

        )

    # -----------------------------------------------------

    def sortino_ratio(
        self,
        annual_return: float,
        downside_volatility: float,
    ) -> float:

        if downside_volatility <= 0:
            return 0.0

        return float(

            (
                annual_return
                - self.risk_free_rate
            )

            / downside_volatility

        )

    # -----------------------------------------------------

    @staticmethod
    def calmar_ratio(
        annual_return: float,
        max_drawdown: float,
    ) -> float:

        if max_drawdown <= 0:
            return 0.0

        return float(
            annual_return
            / max_drawdown
        )

    # -----------------------------------------------------

    @staticmethod
    def information_ratio(
        portfolio_returns: pd.Series,
        benchmark_returns: pd.Series,
    ) -> float:
        """
        Reserved for future benchmark comparison.
        """

        diff = (
            portfolio_returns
            - benchmark_returns
        )

        tracking_error = diff.std()

        if tracking_error == 0:
            return 0.0

        return float(
            diff.mean()
            / tracking_error
        )

    # -----------------------------------------------------

    @staticmethod
    def score(
        sharpe: float,
        sortino: float,
        calmar: float,
    ) -> float:

        score = 0.0

        score += min(
            max(sharpe * 20, 0),
            40,
        )

        score += min(
            max(sortino * 15, 0),
            30,
        )

        score += min(
            max(calmar * 10, 0),
            30,
        )

        return round(
            score,
            2,
        )