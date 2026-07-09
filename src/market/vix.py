"""
India VIX Analyzer
"""

import yfinance as yf


class IndiaVIX:

    SYMBOL = "^INDIAVIX"

    @classmethod
    def analyze(cls):

        df = yf.download(

            cls.SYMBOL,

            period="6mo",

            interval="1d",

            auto_adjust=True,

            progress=False

        )

        if df.empty:

            return None

        # Handle MultiIndex columns
        if hasattr(df.columns, "levels"):

            df.columns = df.columns.get_level_values(0)

        current = float(df["Close"].iloc[-1])

        average = float(df["Close"].mean())

        if current < 13:

            regime = "LOW"

        elif current < 18:

            regime = "NORMAL"

        elif current < 25:

            regime = "HIGH"

        else:

            regime = "EXTREME"

        return {

            "current_vix": round(current, 2),

            "average_vix": round(average, 2),

            "regime": regime

        }