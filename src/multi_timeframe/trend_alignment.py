"""
Multi Timeframe Trend Alignment

Checks trend across multiple timeframes.
"""

import yfinance as yf

from src.indicators.pipeline import IndicatorPipeline


class MultiTimeframeAnalyzer:

    @staticmethod
    def analyze(symbol):

        timeframes = {

            "Monthly": "1mo",

            "Weekly": "1wk",

            "Daily": "1d"

        }

        result = {}

        for timeframe, interval in timeframes.items():

            df = yf.download(

                symbol + ".NS",

                period="2y",

                interval=interval,

                auto_adjust=True,

                progress=False

            )

            if df.empty:

                result[timeframe] = "UNKNOWN"

                continue

            df = IndicatorPipeline.run(df)

            latest = df.iloc[-1]

            ema20 = latest["EMA20"]

            ema50 = latest["EMA50"]

            ema200 = latest["EMA200"]

            if ema20 > ema50 > ema200:

                trend = "BULLISH"

            elif ema20 < ema50 < ema200:

                trend = "BEARISH"

            else:

                trend = "SIDEWAYS"

            result[timeframe] = trend

        return result