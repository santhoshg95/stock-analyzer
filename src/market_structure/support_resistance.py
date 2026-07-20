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
        below_resistance = [r for r in resistances if r <= latest_close]

        # Keep the complete ordered ladder.  A nearby level is an obstacle,
        # not necessarily the end of the move when a breakout is credible.
        raw_resistance_levels = sorted({round(float(level), 4) for level in above_price})
        atr = float(df.iloc[-1].get("ATR", 0) or 0)
        zone_width = max(latest_close * .005, atr * .5)
        resistance_levels = []
        for level in raw_resistance_levels:
            if not resistance_levels or level - resistance_levels[-1] >= zone_width:
                resistance_levels.append(level)
        nearest_resistance = resistance_levels[0] if resistance_levels else None
        next_resistance = resistance_levels[1] if len(resistance_levels) > 1 else None
        broken_resistance = max(below_resistance) if below_resistance else None

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

            "next_resistance": next_resistance,

            "resistance_levels": resistance_levels,

            "broken_resistance": broken_resistance,

            "support_distance": support_distance,

            "resistance_distance": resistance_distance

        }
