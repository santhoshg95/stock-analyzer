"""
Candlestick Pattern Detector

Version 1

Currently supports:

1. Bullish Engulfing
2. Bearish Engulfing
3. Doji
4. Hammer
"""

import pandas as pd


class PatternDetector:

    @staticmethod
    def detect(df: pd.DataFrame):

        if len(df) < 2:

            return {

                "pattern": "UNKNOWN",

                "strength": 0,

                "signal": "NONE"

            }

        prev = df.iloc[-2]

        curr = df.iloc[-1]

        prev_open = float(prev["Open"])
        prev_close = float(prev["Close"])

        open_price = float(curr["Open"])
        close_price = float(curr["Close"])
        high = float(curr["High"])
        low = float(curr["Low"])

        body = abs(close_price - open_price)

        candle_range = high - low

        upper_shadow = high - max(open_price, close_price)

        lower_shadow = min(open_price, close_price) - low

        # ------------------------------------------------
        # Bullish Engulfing
        # ------------------------------------------------

        if (

            prev_close < prev_open

            and close_price > open_price

            and close_price > prev_open

            and open_price < prev_close

        ):

            return {

                "pattern": "BULLISH ENGULFING",

                "strength": 95,

                "signal": "BUY"

            }

        # ------------------------------------------------
        # Bearish Engulfing
        # ------------------------------------------------

        if (

            prev_close > prev_open

            and close_price < open_price

            and open_price > prev_close

            and close_price < prev_open

        ):

            return {

                "pattern": "BEARISH ENGULFING",

                "strength": 95,

                "signal": "SELL"

            }

        # ------------------------------------------------
        # Doji
        # ------------------------------------------------

        if candle_range > 0:

            if body / candle_range < 0.1:

                return {

                    "pattern": "DOJI",

                    "strength": 60,

                    "signal": "NEUTRAL"

                }

        # ------------------------------------------------
        # Hammer
        # ------------------------------------------------

        if (

            lower_shadow > body * 2

            and upper_shadow < body

        ):

            return {

                "pattern": "HAMMER",

                "strength": 85,

                "signal": "BUY"

            }

        return {

            "pattern": "NONE",

            "strength": 0,

            "signal": "NONE"

        }