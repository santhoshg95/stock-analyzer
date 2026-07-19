"""
Return Calculator

Calculates all return-based metrics.

Author:
    AI Research Platform
"""

from __future__ import annotations

import numpy as np
import pandas as pd


class ReturnsCalculator:

    TRADING_DAYS = 252

    def calculate(
        self,
        df: pd.DataFrame,
    ) -> dict:

        df = df.copy()

        close = df["Close"]

        daily_returns = close.pct_change().dropna()

        total_return = (
            close.iloc[-1] / close.iloc[0]
        ) - 1

        years = max(
            len(df) / self.TRADING_DAYS,
            1 / self.TRADING_DAYS,
        )

        cagr = (
            (close.iloc[-1] / close.iloc[0])
            ** (1 / years)
        ) - 1

        annual_return = (
            daily_returns.mean()
            * self.TRADING_DAYS
        )

        weekly_return = (
            daily_returns.mean()
            * 5
        )

        monthly_return = (
            daily_returns.mean()
            * 21
        )

        return {

            "daily_return": float(
                daily_returns.mean()
            ),

            "weekly_return": float(
                weekly_return
            ),

            "monthly_return": float(
                monthly_return
            ),

            "annual_return": float(
                annual_return
            ),

            "total_return": float(
                total_return
            ),

            "cagr": float(
                cagr
            ),
        }

    # ----------------------------------------------------

    def rolling_returns(
        self,
        df: pd.DataFrame,
        window: int = 252,
    ) -> pd.Series:

        close = df["Close"]

        return (
            close
            .pct_change(window)
            .dropna()
        )

    # ----------------------------------------------------

    def monthly_returns(
        self,
        df: pd.DataFrame,
    ) -> pd.Series:

        monthly = (
            df
            .set_index("Date")
            ["Close"]
            .resample("ME")
            .last()
        )

        return monthly.pct_change().dropna()

    # ----------------------------------------------------

    def yearly_returns(
        self,
        df: pd.DataFrame,
    ) -> pd.Series:

        yearly = (
            df
            .set_index("Date")
            ["Close"]
            .resample("YE")
            .last()
        )

        return yearly.pct_change().dropna()

    # ----------------------------------------------------

    def rolling_cagr(
        self,
        df: pd.DataFrame,
        years: int = 3,
    ) -> float:

        trading_days = years * 252

        if len(df) < trading_days:
            return 0.0

        subset = df.tail(trading_days)

        close = subset["Close"]

        return float(

            (
                close.iloc[-1]
                / close.iloc[0]
            )

            ** (1 / years)

            - 1

        )