"""
Volume Indicator

Calculates:
1. Current Volume
2. 20-Day Average Volume
3. Relative Volume (RVOL)
4. Volume Signal
"""

import pandas as pd


class VolumeIndicator:
    """
    Volume Analysis
    """

    @staticmethod
    def calculate(df: pd.DataFrame, period: int = 20) -> pd.DataFrame:
        """
        Calculate volume metrics.

        Parameters
        ----------
        df : pd.DataFrame
            Historical OHLCV Data

        period : int
            Rolling average period

        Returns
        -------
        pd.DataFrame
        """

        data = df.copy()

        # ------------------------------------------
        # Flatten MultiIndex columns (yfinance)
        # ------------------------------------------

        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        # ------------------------------------------
        # Validation
        # ------------------------------------------

        if "Volume" not in data.columns:
            raise ValueError("Volume column not found.")

        # ------------------------------------------
        # Average Volume
        # ------------------------------------------

        data["AVG_VOLUME"] = (
            data["Volume"]
            .rolling(window=period)
            .mean()
        )

        # ------------------------------------------
        # Relative Volume (RVOL)
        # ------------------------------------------

        data["RVOL"] = (
            data["Volume"]
            / data["AVG_VOLUME"]
        )

        # ------------------------------------------
        # Volume Signal
        # ------------------------------------------

        signals = []

        for rvol in data["RVOL"]:

            if pd.isna(rvol):
                signals.append("N/A")

            elif rvol >= 2:
                signals.append("VERY HIGH")

            elif rvol >= 1.2:
                signals.append("HIGH")

            elif rvol >= 0.8:
                signals.append("NORMAL")

            else:
                signals.append("LOW")

        data["VOLUME_SIGNAL"] = signals

        return data