"""
Support & Resistance Engine

Detects swing highs and swing lows to identify
nearest support and resistance levels.
"""

import pandas as pd


class SupportResistanceEngine:

    @staticmethod
    def calculate(df: pd.DataFrame):

        latest_close = float(df.iloc[-1]["Close"])

        highs = df["High"].tolist()
        lows = df["Low"].tolist()

        supports = []
        resistances = []

        # ----------------------------------------------------
        # Detect Swing Highs & Swing Lows
        # ----------------------------------------------------

        for i in range(2, len(df) - 2):

            # Swing High

            if (
                highs[i] > highs[i - 1]
                and highs[i] > highs[i - 2]
                and highs[i] > highs[i + 1]
                and highs[i] > highs[i + 2]
            ):

                resistances.append(highs[i])

            # Swing Low

            if (
                lows[i] < lows[i - 1]
                and lows[i] < lows[i - 2]
                and lows[i] < lows[i + 1]
                and lows[i] < lows[i + 2]
            ):

                supports.append(lows[i])

        # ----------------------------------------------------
        # Nearest Support
        # ----------------------------------------------------

        below_price = [s for s in supports if s < latest_close]

        nearest_support = max(below_price) if below_price else None

        # ----------------------------------------------------
        # Nearest Resistance
        # ----------------------------------------------------

        above_price = [r for r in resistances if r > latest_close]

        nearest_resistance = min(above_price) if above_price else None

        # ----------------------------------------------------
        # Distance Calculations
        # ----------------------------------------------------

        support_distance = None

        resistance_distance = None

        if nearest_support:

            support_distance = round(
                ((latest_close - nearest_support) / latest_close) * 100,
                2
            )

        if nearest_resistance:

            resistance_distance = round(
                ((nearest_resistance - latest_close) / latest_close) * 100,
                2
            )

        return {

            "support": nearest_support,

            "resistance": nearest_resistance,

            "support_distance": support_distance,

            "resistance_distance": resistance_distance

        }